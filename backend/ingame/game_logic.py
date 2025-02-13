import math
import random
import asyncio
import logging
import environ

from django.utils import timezone
from ingame.data import gameid_to_task
from ingame.models import OneVersusOneGame
from pingpong_history.models import PingPongHistory as GameHistory, PingPongRound
from users.models import User
from backend.socketsend import socket_send
from backend.dbAsync import get_game_users
from tournament.models import TournamentGame, TournamentMatchParticipants
from django.db import transaction
from asgiref.sync import sync_to_async
from .enums import Game, GameMode
from tournament.models import Tournament
from ingame.data import user_to_socket

logger = logging.getLogger("django")

env = environ.Env()
# PORT = env("INGAME_PORT") | 3000
PORT = 3000


async def _set_interval(func, interval):
    while True:
        try:
            await func()
        except Exception as e:
            logger.error(e, exc_info=True)
        await asyncio.sleep(interval)


class Vec3:
    """
    커스텀 3d 백터 클래스
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __scale__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __length__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __normalize__(self):
        length = self.__length__()
        if length > 0:
            self.__scale__(1 / length)
        return self


class Ball:
    """
    공 클래스
    """

    def __init__(self, ball_id):
        self.id = ball_id
        self.position = {"x": 0, "y": 6, "z": 0}
        self.velocity = Vec3(0, 0, 0)
        self.summon_direction = True
        self.power_counter = 0
        self.radius = Game.BALL_SIZE.value


class InMemoryGameState:
    """
    게임 상태를 메모리에 저장하는 클래스. 레디스 대신 사용
    """

    game_states = {}

    def __init__(self):
        # In-memory store for game states
        pass

    async def new_game(self, game_id, multi_option=False) -> dict:
        """
        새 게임을 생성하고 초기 상태를 반환
        """
        game_state = {
            "render_data": {
                "oneName": "",
                "twoName": "ai",
                "playerOne": {"x": 0, "y": 6, "z": 100},
                "playerTwo": {"x": 0, "y": 6, "z": -100},
                "balls": [],
                "score": {"playerOne": 0, "playerTwo": 0},
            },
            "game_id": game_id,
            "is_single_player": multi_option is False,
            "ai_KeyState": {"A": False, "D": False},
            "gameStart": False,
            "clients": {},
            # 클라이언트에게 보내지 않는 데이터
            # TODO: 게임 끝날때 보낼 데이터 serializer 에 추가
            "one_keystate": {"A": False, "D": False},
            "two_keystate": {"A": False, "D": False},
            "playerOneId": -1,
            "playerTwoId": -1,
            "rounds": [],  # round = {"rally", "start", "end", "score1", "score2"}
            "current_round_data": {
                "rally": 0,
                "start": None,
                "end": None,
                "score1": 0,
                "score2": 0,
            },
            "current_round": 0,
            "game_start_lock": asyncio.Lock(),
            "key_state_lock": asyncio.Lock(),
            "rally_flag": False,  # paddle to paddle 랠리 확인용 플래그 False = user1, True = user2 면 카운트
            "start_timer": None,
        }
        self.save_game_state(game_id, game_state)
        return game_state

    def save_game_state(self, game_id, state):
        """Save the entire game state."""
        self.game_states[game_id] = state

    def load_game_state(self, game_id):
        """Load the game state."""
        return self.game_states.get(game_id)

    def update_game_state(self, game_id, updates):
        """Update parts of the game state."""
        if game_id in self.game_states:
            self.game_states[game_id] = updates
        else:
            raise KeyError(f"Game ID {game_id} not found.")

    def delete_game_state(self, game_id):
        """Delete the game state after the game ends."""
        if game_id in self.game_states:
            del self.game_states[game_id]
        else:
            raise KeyError(f"Game ID {game_id} not found.")

    @staticmethod
    def reset_current_round(game_state):
        game_state["current_round_data"] = {
            "rally": 0,
            "start": timezone.now(),
            "end": None,
            "score1": 0,
            "score2": 0,
        }

    @staticmethod
    def save_current_round(game_state):
        current_round_data = game_state["current_round_data"]
        current_round_data["score1"] = game_state["render_data"]["score"]["playerOne"]
        current_round_data["score2"] = game_state["render_data"]["score"]["playerTwo"]
        current_round_data["end"] = timezone.now()
        game_state["rounds"].append(current_round_data)
        logger.info("save round data: %s", current_round_data)


class PingPongServer:
    """
    핑퐁 게임 서버 클래스
    """

    def __init__(self, sio):
        self.game_state = InMemoryGameState()
        self.sio = sio

    async def add_user(self, game_id, user, multi_option=False):
        """
        game_id 를 가지고 있는 게임에 유저를 추가
        """
        game_state = self.game_state.load_game_state(game_id)
        if multi_option is False:
            game_state["render_data"]["oneName"] = user.username
            game_state["playerOneId"] = user.id
            return
        user1, user2 = await get_game_users(game_id)
        if user1 and user1.id == user.id:
            game_state["render_data"]["oneName"] = user1.username
            game_state["playerOneId"] = user1.id
        elif user2 and user2.id == user.id:
            game_state["render_data"]["twoName"] = user2.username
            game_state["playerTwoId"] = user2.id

    async def add_game(self, game):
        """
        game_id 가 존재하지 않으면 새 게임을 생성
        """
        ball_count = 2 if game.multi_ball else 1
        game_state = self.game_state.load_game_state(str(game.id))
        if game_state is None:
            game_state = await self.game_state.new_game(
                str(game.id), game.gamemode == GameMode.PVP.value
            )

            for i in range(0, ball_count):
                self._add_ball(game_state)

    async def game_loop(self, game_state):
        """
        게임 루프를 asyncio background task 로 실행
        """
        if game_state["is_single_player"] is False:
            await game_state["start_timer"].cancel()
        logger.info("start game loop")
        game_id = game_state["game_id"]
        game = await GameHistory.objects.aget(id=game_id)
        tournament_id = await self._get_tournament_id(game)
        if tournament_id is not None:
            await Tournament.objects.filter(
                tournament_id=tournament_id.tournament_id
            ).aupdate(status="ongoing", current_round=1)
        InMemoryGameState.reset_current_round(game_state)
        task_list = []
        if game_state["is_single_player"] is True:
            task_list.append(
                asyncio.create_task(
                    _set_interval(
                        lambda: self._update_ai(game_state), Game.AI_INTERVAL.value
                    )
                )
            )
        task_list.append(
            asyncio.create_task(
                _set_interval(
                    lambda: self._update_physics(game_state),
                    Game.PHYSICS_INTERVAL.value,
                )
            )
        )
        task_list.append(
            asyncio.create_task(
                _set_interval(
                    lambda: self._paddle_loop(game_state), Game.PADDLE_INTERVAL.value
                )
            )
        )
        gameid_to_task[game_id] = task_list

    @sync_to_async
    def _get_tournament_id(self, game):
        return game.tournament_id

    def _add_ball(self, game_state) -> None:
        ball_num = len(game_state["render_data"]["balls"])
        ball = Ball(ball_num)
        self._set_ball_velocity(game_state, ball, 1, True)
        game_state["render_data"]["balls"].append(ball)

    def _set_ball_velocity(self, game_state, ball, power_up=1, strat=False):
        angle = (random.random() * 2 - 1) * Game.MAX_ANGLE.value
        direction = 1 if ball.summon_direction else -1
        if strat:
            direction = 1 if len(game_state["render_data"]["balls"]) == 1 else -1
        power_up = 1 if ball.power_counter > 1 else power_up
        ball.power_counter = 1 if power_up == 2 else 0
        vx = math.sin(angle) * Game.CONST_BALL_SPEED.value * power_up
        vz = math.cos(angle) * Game.CONST_BALL_SPEED.value * power_up * direction
        ball.velocity = Vec3(vx, 0, vz)

    async def _update_ai(self, game_state):
        # logger.info("updating ai...")
        ball_position = game_state["render_data"]["balls"]
        target = 0
        if len(ball_position) != 1:
            target = min(
                range(len(ball_position)),
                key=lambda i: ball_position[i].position["z"],
            )

        if ball_position[target].position["x"] < ball_position[target].position["z"]:
            return
        if (
            ball_position[target].position["z"] > 0
            or random.randint(0, 99) < Game.AI_RATE.value
        ):
            return  # ball is over half, or AI decides to not act based on AI_RATE

        if (
            ball_position[target].position["x"]
            < game_state["render_data"]["playerTwo"]["x"]
        ):
            if game_state["ai_KeyState"]["D"]:
                game_state["ai_KeyState"]["D"] = False
            if not game_state["ai_KeyState"]["A"]:
                game_state["ai_KeyState"]["A"] = True
            await self.handle_player_input(game_state, "ai", "A", True)
        else:
            if game_state["ai_KeyState"]["A"]:
                game_state["ai_KeyState"]["A"] = False
            if not game_state["ai_KeyState"]["D"]:
                game_state["ai_KeyState"]["D"] = True
            await self.handle_player_input(game_state, "ai", "D", True)

    async def _update_physics(self, game_state):
        # logger.info("updating physics...")
        if not game_state["gameStart"]:
            return
        game_id = game_state["game_id"]
        # logger.info(f"game_id: {game_id}")
        for ball in game_state["render_data"]["balls"]:
            # Update ball position
            ball.position["x"] += ball.velocity.x * (1 / 60)
            ball.position["y"] += ball.velocity.y * (1 / 60)
            ball.position["z"] += ball.velocity.z * (1 / 60)
            # logger.info(
            #     f"ball velocity: {ball.velocity.x} {ball.velocity.y} {ball.velocity.z}"
            # )

            # Check paddle collisions
            if (
                await self._check_paddle_collision(
                    ball, game_state["render_data"]["playerOne"], game_state
                )
                and not game_state["rally_flag"]
            ):
                current_round_data = game_state["current_round_data"]
                current_round_data["rally"] += 1
                game_state["rally_flag"] = True
            if (
                await self._check_paddle_collision(
                    ball, game_state["render_data"]["playerTwo"], game_state
                )
                and game_state["rally_flag"]
            ):
                current_round_data = game_state["current_round_data"]
                current_round_data["rally"] += 1
                game_state["rally_flag"] = False

            # Check wall collisions
            if abs(ball.position["x"]) > Game.GAME_WIDTH.value / 2 - 2:
                ball.velocity.x *= -1
                await socket_send(
                    game_state["render_data"], "sound", game_id, "ballToWall"
                )

            # Check scoring
            if (
                abs(ball.position["z"]) > Game.GAME_LENGTH.value / 2
                or ball.position["y"] < 0
                or ball.position["y"] > 20
            ):
                if ball.position["z"] > 0:
                    game_state["render_data"]["score"]["playerTwo"] += 1
                    ball.summon_direction = True
                else:
                    game_state["render_data"]["score"]["playerOne"] += 1
                    ball.summon_direction = False
                self._save_round_data(game_state)

                # Check if someone has won the set
                if (
                    game_state["render_data"]["score"]["playerOne"]
                    < Game.GAME_SET_SCORE.value
                    and game_state["render_data"]["score"]["playerTwo"]
                    < Game.GAME_SET_SCORE.value
                ):
                    if game_state["gameStart"]:
                        await socket_send(game_state["render_data"], "score", game_id)
                        self._reset_ball(game_state, ball)
                    return

                winner = (
                    game_state["render_data"]["oneName"]
                    if game_state["render_data"]["score"]["playerOne"]
                    > game_state["render_data"]["score"]["playerTwo"]
                    else game_state["render_data"]["twoName"]
                )
                winner_id = (
                    game_state["playerOneId"]
                    if game_state["render_data"]["score"]["playerOne"]
                    > game_state["render_data"]["score"]["playerTwo"]
                    else game_state["playerTwoId"]
                )

                await game_state["game_start_lock"].acquire()
                if game_state["gameStart"] is False:
                    game_state["game_start_lock"].release()
                    return
                game_state["gameStart"] = False
                game_state["game_start_lock"].release()
                await socket_send(
                    game_state["render_data"],
                    "gameEnd",
                    game_id,
                    f"Winner is {winner}",
                )
                await self._game_finish(game_state, winner_id)
                return

        await self._broadcast_game_state(game_state)

    def _save_round_data(self, game_state):
        InMemoryGameState.save_current_round(game_state)
        InMemoryGameState.reset_current_round(game_state)

    async def _check_paddle_collision(self, ball, paddle, game_state):
        # 1. Find the closest point on the paddle to the ball
        closest_point = {
            "x": max(
                paddle["x"] - Game.PADDLE_WIDTH.value / 2,
                min(ball.position["x"], paddle["x"] + Game.PADDLE_WIDTH.value / 2),
            ),
            "y": max(
                paddle["y"] - Game.PADDLE_HEIGHT.value / 2,
                min(ball.position["y"], paddle["y"] + Game.PADDLE_HEIGHT.value / 2),
            ),
            "z": max(
                paddle["z"] - Game.PADDLE_DEPTH.value / 2,
                min(ball.position["z"], paddle["z"] + Game.PADDLE_DEPTH.value / 2),
            ),
        }

        # 2. Calculate the distance between the ball's center and the closest point on the paddle
        distance = math.sqrt(
            (ball.position["x"] - closest_point["x"]) ** 2
            + (ball.position["y"] - closest_point["y"]) ** 2
            + (ball.position["z"] - closest_point["z"]) ** 2
        )

        # 3. If the distance is less than or equal to the ball's radius, it's a collision
        if distance <= Game.BALL_SIZE.value:
            await socket_send(game_state["render_data"], "sound", "ballToWall")
            hit_point_diff = ball.position["x"] - paddle["x"]
            max_bounce_angle = math.pi / 3
            bounce_angle = (hit_point_diff / 10) * max_bounce_angle
            speed = Vec3(ball.velocity.x, ball.velocity.y, ball.velocity.z).__length__()
            direction = -1 if ball.position["z"] < paddle["z"] else 1

            # Update ball's velocity after the collision
            ball.velocity.x = math.sin(bounce_angle) * speed
            ball.velocity.z = math.cos(bounce_angle) * speed * direction
            ball.velocity.y = min(ball.velocity.y, 0)
            return True

    async def check_powerball(self, game_state, data):
        """
        스페이스 입력시 파워볼인지 확인하고 파워볼이면 공의 속도를 높임
        """
        game_id = game_state["game_id"]
        player = (
            game_state["render_data"]["playerOne"]
            if not data.get("who")
            else game_state["render_data"]["playerTwo"]
        )

        is_collision = [
            ball
            for ball in game_state["render_data"]["balls"]
            if self._is_in_range(int(ball.position["x"]), int(player["x"]), 10)
            and self._is_in_range(int(ball.position["z"]), int(player["z"]), 10)
        ]
        if len(is_collision) == 1:
            self._set_ball_velocity(game_state, is_collision[0], 2)
            logger.info(f"Collision: {is_collision[0].position}")
            await socket_send(
                game_state["render_data"],
                "effect",
                game_id,
                is_collision[0].position,
            )

    def _is_in_range(self, number, target, range):
        return abs(number - target) <= range

    def _reset_ball(self, game_state, ball):
        ball.position = {"x": 0, "y": 5, "z": 0}
        ball.power_counter = 0
        self._set_ball_velocity(game_state, ball)

    def reset_all_balls(self, game_state):
        for ball in game_state["balls"]:
            self._reset_ball(game_state, ball)

    def _handle_ai_input(self, game_state, key, pressed):
        player = game_state["render_data"]["playerTwo"]
        if key == "A" and pressed:
            player["x"] -= Game.MOVE_SPEED.value
        elif key == "D" and pressed:
            player["x"] += Game.MOVE_SPEED.value

        player["x"] = max(
            -Game.GAME_WIDTH.value / 2 + 10,
            min(Game.GAME_WIDTH.value / 2 - 10, player["x"]),
        )

    async def _broadcast_game_state(self, game_state):
        # logger.info("Broadcasting game state...")
        game_id = game_state["game_id"]
        await socket_send(game_state["render_data"], "gameState", game_id)

    async def handle_player_input(self, game_state, player_id, key, pressed):
        # logger.info(f"player_id: {player_id}")
        # logger.info(f"user1: {game_state['playerOneId']}")
        # logger.info(f"user2: {game_state['playerTwoId']}")

        # logger.info(f"key???: {key}")
        await game_state["key_state_lock"].acquire()
        if player_id == "ai":
            # AI 플레이어의 입력 처리
            logger.info(f"AI key state: {game_state['two_keystate']}")
            self._handle_ai_input(game_state, key, pressed)
        elif player_id == game_state["playerOneId"]:
            # 첫 번째 플레이어의 입력 처리
            game_state["one_keystate"][key] = pressed
        elif player_id == game_state["playerTwoId"]:
            # 두 번째 플레이어의 입력 처리
            game_state["two_keystate"][key] = pressed
        else:
            logger.warning(f"Unknown player ID: {player_id}")
            # 플레이어 ID를 찾을 수 없으므로 처리하지 않음
        game_state["key_state_lock"].release()

    async def _paddle_loop(self, game_state):
        player_one = game_state["render_data"]["playerOne"]
        one_name = game_state["render_data"]["oneName"]
        player_two = game_state["render_data"]["playerTwo"]
        two_name = game_state["render_data"]["twoName"]
        await self._process_paddle_move(
            game_state, one_name, player_one, game_state["one_keystate"]
        )
        await self._process_paddle_move(
            game_state, two_name, player_two, game_state["two_keystate"]
        )

    async def _process_paddle_move(self, game_state, player_name, player, key):
        if player_name == "ai":
            return
        await game_state["key_state_lock"].acquire()
        # logger.info(f"key: {key}")
        if key["A"] and key["D"]:
            game_state["key_state_lock"].release()
            return
        if key["A"]:
            # logger.info("move left")
            player["x"] -= Game.MOVE_SPEED.value
        elif key["D"]:
            # logger.info("move right")
            player["x"] += Game.MOVE_SPEED.value
        game_state["key_state_lock"].release()
        # 플레이어의 위치가 게임 영역을 벗어나지 않도록 제한
        player["x"] = max(
            -Game.GAME_WIDTH.value / 2 + 10,
            min(Game.GAME_WIDTH.value / 2 - 10, player["x"]),
        )

    async def _game_finish(self, game_state, winner_id):
        await self.save_game_history(game_state, winner_id)
        game = await GameHistory.objects.aget(id=game_state["game_id"])
        game_id = game_state["game_id"]
        tournament = await self._get_tournament_id(game)
        if tournament is not None:
            await sync_to_async(self.update_tournament)(game, winner_id)
        logger.info("Game finished: %s", game_id)
        logger.info("is_single_player: %s", game_state["is_single_player"])
        if game_state["is_single_player"] is False:
            await self._clean_one_v_one_game(game_id)

        self.game_state.delete_game_state(game_id)

        # 게임 종료 후 클라이언트 소켓 연결 종료
        user1, user2 = await get_game_users(game_id)
        if user1.id in user_to_socket:
            sid1 = user_to_socket[user1.id]
            self.sio.disconnect(sid1)
            del user_to_socket[user1.id]
        if user2 is not None and user2.id in user_to_socket:
            sid2 = user_to_socket[user2.id]
            self.sio.disconnect(sid2)
            del user_to_socket[user2.id]

        # clean up tasks
        task_list = gameid_to_task[game_id]
        for task in task_list:
            task.cancel()
        del gameid_to_task[game_id]

    def update_tournament(self, game, winner_id):
        TournamentGame.objects.filter(game_id=game.id).update(
            status="finished",
            ended_at=timezone.now(),
            winner_id=winner_id,
        )
        GameHistory.objects.filter(id=game.id).update(
            ended_at=timezone.now(), winner_id=winner_id
        )
        with transaction.atomic():
            tournament_game = TournamentGame.objects.get(game_id=game.id)
            tournament = game.tournament_id
            winner = None if winner_id is None else User.objects.get(id=winner_id)
            if tournament.current_game == 1:
                tournament.round_1_winner = winner
            elif tournament.current_game == 2:
                tournament.round_2_winner = winner
                tournament.current_round = 2
                tournament_game.tournament_round = 2
            else:
                tournament.round_3_winner = winner
                tournament.status = "finished"
            tournament.current_game += 1
            tournament.save()
            tournament_game.save()

        if tournament.status == "finished":
            return
        tournament_participants = TournamentMatchParticipants.objects.get(
            tournament_id=tournament
        )
        # 다음 라운드 생성
        if tournament.current_round == 1:
            user1 = tournament_participants.user3
            user2 = tournament_participants.user4
            logger.info("round 1")
            logger.info("user: %s", user1)
            logger.info("user: %s", user2)
            next_round = 1
        else:
            next_round = 2
            user1 = tournament.round_1_winner
            user2 = tournament.round_2_winner
            logger.info("round 2")
            logger.info("user: %s", user1)
            logger.info("user: %s", user2)
        if user1 is None and user2 is None:
            return
        game_id = GameHistory.objects.create(
            user1=user1,
            user2=user2,
            gamemode=GameMode.PVP.value,
            tournament_id=tournament,
            option_selector_id=tournament_participants.user1_id,
            multi_ball=tournament.multi_ball,
        )
        TournamentGame.objects.create(
            game_id=game_id,
            tournament_id=tournament,
            tournament_round=next_round,
            user_1=user1,
            user_2=user2,
            status="ongoing",
        )
        if user1 is None or user2 is None:
            winner = user1 if user1 is not None else user2
            self.update_tournament(game_id, winner.id)

    async def _clean_one_v_one_game(self, game_id):
        try:
            await OneVersusOneGame.objects.filter(game_id=game_id).adelete()
        except OneVersusOneGame.DoesNotExist:
            logger.info("Game not found: %s", game_id)

    async def process_abandoned_game(self, game_state):
        """
        게임이 종료되지 않은 상태에서 모든 플레이어가 게임을 나갔을 때 호출
        """
        logger.info("Abandoned game: %s", game_state["game_id"])
        game_id = game_state["game_id"]
        await self.save_game_history(game_state, None)
        game = await GameHistory.objects.aget(id=game_id)
        if await self._get_tournament_id(game) is not None:
            await sync_to_async(self.update_tournament)(game, None)
        await self._clean_one_v_one_game(game_id)
        self.game_state.delete_game_state(game_id)

        user1, user2 = await get_game_users(game_id)
        if user1.id in user_to_socket:
            sid1 = user_to_socket[user1.id]
            self.sio.disconnect(sid1)
            del user_to_socket[user1.id]
        if user2.id != -1 and user2.id in user_to_socket:
            sid2 = user_to_socket[user2.id]
            self.sio.disconnect(sid2)
            del user_to_socket[user2.id]

        await socket_send(
            game_state["render_data"], "gameEnd", game_id, "Game abandoned"
        )
        task_list = gameid_to_task[game_id]
        for task in task_list:
            task.cancel("abandoned cancel")

    async def save_game_history(self, game_state, winner_id):
        game_id = game_state["game_id"]
        game = await GameHistory.objects.aget(id=game_id)
        logger.info("winner: %s", winner_id)
        winner = (
            None
            if (winner_id is None) or (winner_id == -1)
            else await User.objects.aget(id=winner_id)
        )
        await self._save_pingpong_history(game_state, winner, game)
        await self._update_rounds(game_state)
        if game.gamemode == GameMode.PVP.value:
            self._update_wins_losses(game, winner)

    async def _save_pingpong_history(self, game_state, winner, game):
        if len(game_state["rounds"]) == 0:
            all_rallies = [game_state["current_round_data"]["rally"]]
        else:
            all_rallies = [round_data["rally"] for round_data in game_state["rounds"]]
        longest_rally = max(all_rallies)
        average_rally = sum(all_rallies) / len(all_rallies)
        # Save game history
        game.winner = winner
        game.ended_at = timezone.now()
        game.user1_score = game_state["render_data"]["score"]["playerOne"]
        game.user2_score = game_state["render_data"]["score"]["playerTwo"]
        game.longest_rally = longest_rally
        game.average_rally = average_rally
        await game.asave()

    def _update_wins_losses(self, game, winner):
        if game.ended_at is None:
            winner = None
        asyncio.gather(
            self._update_wins_losses(game.user1, winner),
            self._update_wins_losses(game.user2, winner),
        )

    async def _update_rounds(self, game_state):
        rounds = game_state["rounds"]
        game_id = game_state["game_id"]
        round_list = []
        for _round in rounds:
            round_model = PingPongRound(
                match_id=game_id,
                user1_score=_round["score1"],
                user2_score=_round["score2"],
                rally=_round["rally"],
                start=_round["start"],
                end=_round["end"],
            )
            round_list.append(round_model)
        await PingPongRound.objects.abulk_create(round_list)

    async def _update_wins_losses(self, user, winner):
        if winner is None:
            user.loses += 1
            await user.asave()
            return
        if user == winner:
            user.wins += 1
        else:
            user.loses += 1
        await user.asave()
