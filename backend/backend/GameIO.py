import asyncio

from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import logging
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
    TokenBackendError,
)
from django.conf import settings
import socketio

from pingpong_history.models import PingPongHistory
from ingame.game_logic import PingPongServer
from ingame.data import user_to_game, user_to_socket
from ingame.models import OneVersusOneGame
from ingame.enums import GameMode
from users.models import User

from backend.socketsend import socket_send, DEFAULT_NAMESPACE
from backend.sio import sio
from backend.dbAsync import get_game_users
from .background_timer import CancellableTimer

from asgiref.sync import sync_to_async

logger = logging.getLogger("django")

server = PingPongServer(sio)
game_state_db = server.game_state
# mock_game_id = str(uuid.uuid4())  # Example: 'e4d909c2-6b18-11ed-81ce-0242ac120002'


class GameIO(socketio.AsyncNamespace):
    """
    게임 통신을 위한 SocketIO 네임스페이스
    """

    async def on_connect(self, sid, environ, auth):
        """
        클라이언트가 연결되었을 때 호출되는 메서드
        """
        # logger.info(f"Client connected: {sid} {auth}")
        if await self._check_authentication(environ, sid) is False:
            sio.disconnect(sid)
            return False

        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user = session["user"]

        # 여러 소켓이 하나의 유저로 들어올 경우
        if user.id in user_to_socket:
            logger.info("multiple user socket")
            sio.disconnect(sid)
            return

        query = environ.get("QUERY_STRING", "")
        params = parse_qs(query)
        game_id = params.get("gameId", [""])[0]
        try:
            int(game_id)
            game: PingPongHistory = await PingPongHistory.objects.aget(id=game_id)
        except Exception as e:
            # logger.error(str(e), exc_info=True)
            sio.disconnect(sid)
            return

        if not game or game.ended_at is not None:
            logger.info("Game already ended: %s", game_id)
            await sio.emit(
                "gameEnd", room=sid, namespace="/api/game"
            )  # TODO: 게임이 끝났다고 알림
            sio.disconnect(sid)
            return
        # upon successful authentication, enter game room
        await sio.enter_room(sid, game_id, namespace="/api/game")
        try:
            if (
                await self._process_authorization(sid, game_id, game.gamemode, game)
                is False
            ):
                logger.info("Authorization failed: %s", game_id)
                return
        except OneVersusOneGame.DoesNotExist:
            logger.info("Game not found: %s", game_id)
            sio.disconnect(sid)
            return

        user_to_socket[user.id] = sid
        # enter game room
        # save user sid to game_id
        user_to_game[sid] = game_id
        if game.gamemode == GameMode.PVE.value:
            await server.add_game(game)
            await server.add_user(game_id, user, game.gamemode == GameMode.PVP.value)
        else:
            # 게임이 존재하지 않을 경우 연결 종료
            user1, user2 = await get_game_users(game_id)
        # add user's active socket to user_to_socket
        if game.gamemode == GameMode.PVP.value:
            await server.add_game(game)  # 유저이름 변경 필요 받아야 할듯
            await server.add_user(game_id, user, game.gamemode == GameMode.PVP.value)

        game_state = game_state_db.load_game_state(game_id)
        game_state["clients"][sid] = sid

        if game.gamemode == GameMode.PVE.value:
            await self._single_player_start(game_id)
            return
        # PVP logic
        if len(game_state["clients"]) > 1:
            await self._on_game_ready(user2, user, game_state, sid)
        else:
            await self._on_first_user_enter(user2, user, game_state, sid)

        await socket_send(game_state["render_data"], "gameState", sid, game_id)

    async def on_keypress(self, sid, data):
        """
        클라이언트로부터 키 입력을 받았을 때 호출되는 메서드
        """
        logger.info("Key press: %s", data)
        if sid not in user_to_game:
            logger.info("User not in game: %s", sid)
            return
        game_id = user_to_game[sid]
        game_state = server.game_state.load_game_state(game_id)
        if game_state["gameStart"] is False:
            return
        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user = session["user"]
        logger.info("user_id: %s", user.id)

        if data["key"] != " ":
            await server.handle_player_input(
                game_state, user.id, data["key"], data["pressed"]
            )
        else:
            await server.check_powerball(game_state, data)

    async def on_disconnect(self, sid):
        """
        클라이언트 연결이 끊겼을 때 호출되는 메서드
        """
        logger.info("Client disconnected: %s", sid)
        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user = session["user"]
        # user.id 는 바뀌지 않음
        if user.id in user_to_socket:
            del user_to_socket[user.id]
        # 유저가 spectator 유저일 경우 user_to_game 을 등록하지 않음
        if sid not in user_to_game:
            return
        game_id = user_to_game[sid]
        game_state = game_state_db.load_game_state(game_id)

        # 게임이 종료되었을 경우
        if game_state is None:
            return

        if sid in game_state["clients"]:
            del game_state["clients"][sid]

        game = await PingPongHistory.objects.aget(id=game_id)
        # 게임이 진행중이고고 클라이언트가 모두 나갔을 경우 게임 종료
        await game_state["game_start_lock"].acquire()
        if (
            len(game_state["clients"]) == 0
            and game_state["gameStart"] is True
            and game.gamemode == GameMode.PVP.value
        ):
            game_state["gameStart"] = False
            await server.process_abandoned_game(game_state)
        game_state["game_start_lock"].release()
        del user_to_game[sid]

    ### helper functions

    async def _check_authentication(self, environ, sid):
        cookies = environ.get("HTTP_COOKIE", "")
        cookie = SimpleCookie()
        cookie.load(cookies)

        logger.info("cookie: %s", cookie)

        token = cookie.get(settings.REST_AUTH["JWT_AUTH_COOKIE"])
        if not token:
            logger.info("Authentication failed: No token found in cookies")
            return False
        try:
            token_backend = TokenBackend(
                algorithm="HS256", signing_key=settings.SECRET_KEY
            )
            validated_data = token_backend.decode(token.value)
            logger.info("User authenticated: %s", validated_data)
            user = await User.objects.aget(id=validated_data["user_id"])
            await sio.save_session(sid, {"user": user}, namespace=DEFAULT_NAMESPACE)
        except Exception as e:
            logger.info("%s", str(e))
            return False  # Deny the connection

        logger.info("Connection allowed")
        return True  # Allow the connection

    async def _check_authorization(self, sid, game_id):
        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user = session["user"]
        user_1, user_2 = await get_game_users(game_id)
        if user in [user_1, user_2]:
            logger.info("Authorization success: %s in %s", user, game_id)
            return True
        logger.info("Authorization failed: %s not in %s", user, game_id)
        return False

    async def _process_authorization(self, sid, game_id, game_type, game):
        if game_type == GameMode.PVE.value:
            return await self._pve_authorization(sid, game_id)
        if not await self._check_authorization(sid, game_id):
            return False

            # enter spectator mode
        game_state = game_state_db.load_game_state(game_id)
        if game_state and game_state["gameStart"] is True:
            await socket_send(game_state["render_data"], "gameStart", sid, game_id)
        return True

    async def _pve_authorization(self, sid, game_id):
        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user: User = session["user"]
        try:
            await PingPongHistory.objects.aget(id=game_id, user1=user)
        except PingPongHistory.DoesNotExist:
            logger.info("PingPongHistory not found: %s", game_id)
            return False

    async def _on_game_ready(self, user2, user, game_state, sid):
        logger.info("Two players are ready!")
        game_id = game_state["game_id"]
        if user2 == user:
            await socket_send(game_state["render_data"], "secondPlayer", game_id, sid)
        await socket_send(game_state["render_data"], "gameStart", game_id)
        if game_state["gameStart"] is False:
            await server.game_loop(game_state)
        game_state["gameStart"] = True

    async def _on_first_user_enter(self, user2, user, game_state, sid):
        game_id = game_state["game_id"]
        game_state["start_timer"] = CancellableTimer(
            5, self._single_player_end, game_id, sid
        )
        game_state["start_timer"].start()
        if user2 == user:
            await socket_send(game_state["render_data"], "secondPlayer", game_id, sid)
        logger.info("Waiting for another player...")
        await socket_send(game_state["render_data"], "gameWait", game_id, sid)

    async def _single_player_start(self, game_id):
        game_state = game_state_db.load_game_state(game_id)
        await socket_send(game_state["render_data"], "gameStart", game_id)
        logger.info("Single player game start")
        if game_state["gameStart"] is False:
            await server.game_loop(game_state)
        game_state["gameStart"] = True

    async def _single_player_end(self, game_id, sid):
        game_state = game_state_db.load_game_state(game_id)
        await socket_send(game_state["render_data"], "gameEnd", game_id)
        logger.info("Single player game end")
        game_state["gameStart"] = False
        session = await sio.get_session(sid, namespace=DEFAULT_NAMESPACE)
        user = session["user"]
        try:
            game = await PingPongHistory.objects.aget(id=game_id)
            logger.info("Game ended: %s", game_id)
            await OneVersusOneGame.objects.filter(game_id=game_id).adelete()
            if self._get_tournament_id(game) is not None:
                await server.update_tournament(game, user.id)
            else:
                await server.save_game_history(game_state, user.id)
        except Exception as e:
            logger.error(str(e), exc_info=True)
        game_state_db.delete_game_state(game_id)
        logger.info("Game state deleted")
        return

    @sync_to_async
    def _get_tournament_id(self, game):
        return game.tournament_id
