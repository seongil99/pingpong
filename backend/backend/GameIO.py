from http.cookies import SimpleCookie
from urllib.parse import parse_qs
import logging
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
    TokenBackendError,
)
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
import socketio

from pingpong_history.models import PingPongHistory
from ingame.game_logic import PingPongServer
from ingame.data import user_to_game, user_to_socket
from ingame.models import OneVersusOneGame
from ingame.enums import GameMode

from backend.socketsend import socket_send, default_namespace
from backend.sio import sio
from backend.dbAsync import get_game_users


logger = logging.getLogger("django")
User = get_user_model()

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
        if await self.check_authentication(environ, sid) is False:
            sio.disconnect(sid)
            return False

        query = environ.get("QUERY_STRING", "")
        params = parse_qs(query)
        game_id = params.get("gameId", [""])[0]
        game = await PingPongHistory.objects.aget(id=game_id)
        game_type = game.gamemode
        if game.ended_at is not None:
            logger.info("Game already ended: %s", game_id)
            sio.emit(
                "gameEnd", room=sid, namespace="/api/game"
            )  # TODO: 게임이 끝났다고 알림
            sio.disconnect(sid)
            return
        # upon successful authentication, enter game room
        await sio.enter_room(sid, game_id, namespace="/api/game")
        try:
            if await self.process_authorization(sid, game_id, game_type) is False:
                return
        except OneVersusOneGame.DoesNotExist:
            logger.info("Game not found: %s", game_id)
            sio.disconnect(sid)
            return

        session = await sio.get_session(sid, namespace=default_namespace)
        user = session["user"]

        # 여러 소켓이 하나의 유저로 들어올 경우
        if user.id in user_to_socket:
            sio.disconnect(sid)
            return
        user_to_socket[user.id] = sid
        # enter game room

        # save user sid to game_id
        user_to_game[sid] = game_id
        if game_type == GameMode.PVE.value:
            await server.add_game(game_id, game_type == GameMode.PVP.value)
            await server.add_user(game_id, user, game_type == GameMode.PVP.value)
        else:
            # 게임이 존재하지 않을 경우 연결 종료
            user1, user2 = await get_game_users(game_id)
        # add user's active socket to user_to_socket
        if game_type == GameMode.PVP.value:
            await server.add_game(
                game_id, game_type == "PVP"
            )  # 유저이름 변경 필요 받아야 할듯
            await server.add_user(game_id, user, game_type == "PVP")
        game_state = game_state_db.load_game_state(game_id)
        game_state["clients"][sid] = sid
        logger.info("game_state: %s", game_state)
        if game_type == GameMode.PVE.value:
            await self.single_player_start(game_id)
            return
        # PVP logic
        if len(game_state["clients"]) > 1:
            await self.on_game_ready(user2, user, game_state, sid)
        else:
            await self.on_first_user_enter(user2, user, game_state, sid)

        await socket_send(game_state["render_data"], "gameState", sid, game_id)

    async def on_keypress(self, sid, data):
        """
        클라이언트로부터 키 입력을 받았을 때 호출되는 메서드
        """
        logger.info(f"Key press: {data}")
        if sid not in user_to_game:
            logger.info(f"User not in game: {sid}")
            return
        game_id = user_to_game[sid]
        game_state = server.game_state.load_game_state(game_id)
        if game_state["gameStart"] == False:
            return
        session = await sio.get_session(sid, namespace=default_namespace)
        user = session["user"]
        logger.info(f"user_id: {user.id}")

        if data["key"] != " ":
            await server.handle_player_input(
                game_state, user.id, data["key"], data["pressed"]
            )
        else:
            await server.check_powerball(game_state, data)

    async def on_disconnect(self, sid):
        logger.info(f"Client disconnected: {sid}")
        session = await sio.get_session(sid, namespace=default_namespace)
        user = session["user"]
        if user.id in user_to_socket:
            del user_to_socket[user.id]
        if sid not in user_to_game:
            return
        game_id = user_to_game[sid]
        game_state = game_state_db.load_game_state(game_id)

        # 게임이 종료되었을 경우
        if game_state == None:
            return

        if sid in game_state["clients"]:
            del game_state["clients"][sid]

        game = await PingPongHistory.objects.aget(id=game_id)
        # 게임이 진행중이고고 클라이언트가 모두 나갔을 경우 게임 종료
        if (
            len(game_state["clients"]) == 0
            and game_state["gameStart"] == True
            and game.gamemode == GameMode.PVP.value
        ):
            await server.process_abandoned_game(game_state)
        del user_to_game[sid]

    ### helper functions

    async def check_authentication(self, environ, sid):
        cookies = environ.get("HTTP_COOKIE", "")
        cookie = SimpleCookie()
        cookie.load(cookies)

        logger.info(f"cookie: {cookie}")

        token = cookie.get(settings.REST_AUTH["JWT_AUTH_COOKIE"])
        if not token:
            logger.info("Authentication failed: No token found in cookies")
            return False
        SECRET_KEY = settings.SECRET_KEY
        try:
            token_backend = TokenBackend(algorithm="HS256", signing_key=SECRET_KEY)
            validated_data = token_backend.decode(token.value)
            logger.info(f"User authenticated: {validated_data}")
            user = await get_user(validated_data["user_id"])
            await sio.save_session(sid, {"user": user}, namespace=default_namespace)
        except (InvalidToken, TokenError, TokenBackendError) as e:
            logger.info(f"Invalid token: {str(e)}")
            return False  # Deny the connection

        logger.info("Connection allowed")
        return True  # Allow the connection

    async def check_authorization(self, sid, game_id):
        session = await sio.get_session(sid, namespace=default_namespace)
        user = session["user"]
        user_1, user_2 = await get_game_users(game_id)
        if user in [user_1, user_2]:
            logger.info(f"Authorization success: {user} in {game_id}")
            return True
        logger.info(f"Authorization failed: {user} not in {game_id}")
        return False

    async def process_authorization(self, sid, game_id, gameType):
        if gameType == GameMode.PVE.value:
            return await self.pve_authorization(sid, game_id)
        if not await self.check_authorization(sid, game_id):
            return False

            # enter spectator mode
        game_state = game_state_db.load_game_state(game_id)
        if game_state and game_state["gameStart"] == True:
            await socket_send(game_state["render_data"], "gameStart", sid, game_id)
        return True

    async def pve_authorization(self, sid, game_id):
        session = await sio.get_session(sid, namespace=default_namespace)
        user = session["user"]
        try:
            pingpong_history = await PingPongHistory.objects.aget(id=game_id)
        except PingPongHistory.DoesNotExist:
            logger.info(f"PingPongHistory not found: {game_id}")
            return False
        await self.is_pve_auth_condition_valid(user, pingpong_history)

    @sync_to_async
    def is_pve_auth_condition_valid(self, user, pingpong_history):
        return (
            pingpong_history
            and pingpong_history.user1 == user
            and not pingpong_history.ended_at
        )

    async def on_game_ready(self, user2, user, game_state, sid):
        logger.info("Two players are ready!")
        game_id = game_state["game_id"]
        if user2 == user:
            await socket_send(game_state["render_data"], "secondPlayer", game_id, sid)
        await socket_send(game_state["render_data"], "gameStart", game_id)
        if game_state["gameStart"] == False:
            server.game_loop(game_state)
        game_state["gameStart"] = True

    async def on_first_user_enter(self, user2, user, game_state, sid):
        game_id = game_state["game_id"]
        if user2 == user:
            await socket_send(game_state["render_data"], "secondPlayer", game_id, sid)
        logger.info("Waiting for another player...")
        await socket_send(game_state["render_data"], "gameWait", game_id, sid)

    async def single_player_start(self, game_id):
        game_state = game_state_db.load_game_state(game_id)
        await socket_send(game_state["render_data"], "gameStart", game_id)
        logger.info("Single player game start")
        if game_state["gameStart"] == False:
            server.game_loop(game_state)
        game_state["gameStart"] = True


@sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
