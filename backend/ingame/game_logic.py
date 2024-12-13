import environ
import math
import random
import time
import asyncio
from backend.socketsend import socket_send
from ingame.data import gameid_to_task
from backend.dbAsync import get_game_users, delete_game
from pingpong_history.models import PingPongHistory as GameHistory
from .enums import KeyState
from django.utils import timezone
from asgiref.sync import sync_to_async

from .enums import Game
import logging

logger = logging.getLogger("django")

env = environ.Env()
# PORT = env("INGAME_PORT") | 3000
PORT = 3000


async def set_interval(func, interval):
    while True:
        start_time = time.perf_counter()
        await func()
        elapsed_time = (
            time.perf_counter() - start_time
        ) * 1_000_000  # Convert to microseconds
        await asyncio.sleep(interval)


# Example usage:
def print_message():
    print("This function runs every 0.5 seconds.")


# Run the async function
# asyncio.run(set_interval(print_message, 0.5))  # Calls `print_message` every 0.5 seconds


class Vec3:
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
        len = self.length()
        if len > 0:
            self.scale(1 / len)
        return self


class Ball:
    def __init__(self, id):
        self.id = id
        self.position = {"x": 0, "y": 6, "z": 0}
        self.velocity = Vec3(0, 0, 0)
        self.summon_direction = True
        self.powerCounter = 0
        self.radius = Game.BALL_SIZE.value


class InMemoryGameState:
    game_states = {}

    def __init__(self):
        # In-memory store for game states
        pass

    async def new_game(self, game_id, multiOption=False) -> dict:
        game_state = {
            "render_data": {
                "oneName": "",
                "twoName": "ai",
                "playerOne": {"x": 0, "y": 6, "z": 100},
                "playerTwo": {"x": 0, "y": 6, "z": -100},
                "balls": [],
                "score": {"playerOne": 0, "playerTwo": 0},
            },
            "one_keystate": {"A": False, "D": False},
            "two_keystate": {"A": False, "D": False},
            "is_single_player": multiOption == False,
            "ai_KeyState": {"A": False, "D": False},
            "gameStart": False,
            "playerOneId": "",
            "playerTwoId": "",
            "clients": {},
            "rallies": [],
            "current_rally": 0,
            "game_id": game_id,
            "key_state_lock": asyncio.Lock(),
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

    def generate_game_id(self):
        return "game_" + str(len(self.game_states) + 1)


class PingPongServer:
    def __init__(self, sio):
        self.game_state = InMemoryGameState()
        self.sio = sio

    async def add_user(self, game_id, user, multiOption=False):
        game_state = self.game_state.load_game_state(game_id)

        logger.info(f"user: {user}")
        if multiOption == False:
            game_state["render_data"]["oneName"] = user.username
            game_state["playerOneId"] = user.id
            return
        user1, user2 = await get_game_users(game_id)
        if user1.id == user.id:
            game_state["render_data"]["oneName"] = user1.username
            game_state["playerOneId"] = user1.id
        elif user2.id == user.id:
            game_state["render_data"]["twoName"] = user2.username
            game_state["playerTwoId"] = user2.id

    async def add_game(
        self, game_id, multi_option, ballCount=1
    ):  # user_id == user_name, player_id == user.id -> pk
        # if game doesn't exist == User1
        game_state = self.game_state.load_game_state(game_id)
        if game_state == None:
            game_state = await self.game_state.new_game(game_id, multi_option)
            for i in range(0, ballCount):
                self.addBall(game_state)

    def game_loop(self, game_state):
        game_id = game_state["game_id"]
        task_list = []
        if game_state["is_single_player"] == True:
            task_list.append(
                asyncio.create_task(
                    set_interval(
                        lambda: self.update_ai(game_state), Game.AI_INTERVAL.value
                    )
                )
            )
        task_list.append(
            asyncio.create_task(
                set_interval(
                    lambda: self.update_physics(game_state), Game.PHYSICS_INTERVAL.value
                )
            )
        )
        task_list.append(
            asyncio.create_task(
                set_interval(
                    lambda: self.paddle_loop(game_state), Game.PADDLE_INTERVAL.value
                )
            )
        )
        gameid_to_task[game_id] = task_list

    def addBall(self, game_state) -> None:
        ballNum = len(game_state["render_data"]["balls"])
        ball = Ball(ballNum)
        self.set_ball_velocity(game_state, ball, 1, True)
        game_state["render_data"]["balls"].append(ball)

    def set_ball_velocity(self, game_state, ball, powerUp=1, strat=False):
        MAX_ANGLE = math.pi / 6
        ANGLE = (random.random() * 2 - 1) * MAX_ANGLE
        direction = 1 if ball.summon_direction else -1
        if strat:
            direction = 1 if len(game_state["render_data"]["balls"]) == 1 else -1
        powerUp = 1 if ball.powerCounter > 1 else powerUp
        ball.powerCounter = 1 if powerUp == 2 else 0
        vx = math.sin(ANGLE) * Game.CONST_BALL_SPEED.value * powerUp
        vz = math.cos(ANGLE) * Game.CONST_BALL_SPEED.value * powerUp * direction
        ball.velocity = Vec3(vx, 0, vz)

    async def update_ai(self, game_state):
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

    async def update_physics(self, game_state):
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
            await self.check_paddle_collision(
                ball, game_state["render_data"]["playerOne"], game_state
            )
            await self.check_paddle_collision(
                ball, game_state["render_data"]["playerTwo"], game_state
            )

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
                game_state["rallies"].append(game_state["current_rally"])
                game_state["current_rally"] = 0
                if ball.position["z"] > 0:
                    game_state["render_data"]["score"]["playerTwo"] += 1
                    ball.summon_direction = True
                else:
                    game_state["render_data"]["score"]["playerOne"] += 1
                    ball.summon_direction = False

                # Check if someone has won the set
                if (
                    game_state["render_data"]["score"]["playerOne"]
                    >= Game.GAME_SET_SCORE.value
                    or game_state["render_data"]["score"]["playerTwo"]
                    >= Game.GAME_SET_SCORE.value
                ):
                    winner = (
                        game_state["render_data"]["oneName"]
                        if game_state["render_data"]["score"]["playerOne"]
                        > game_state["render_data"]["score"]["playerTwo"]
                        else game_state["render_data"]["twoName"]
                    )
                    winnerId = (
                        game_state["playerOneId"]
                        if game_state["render_data"]["score"]["playerOne"]
                        > game_state["render_data"]["score"]["playerTwo"]
                        else game_state["playerTwoId"]
                    )
                    await socket_send(
                        game_state["render_data"],
                        "gameEnd",
                        game_id,
                        f"Winner is {winner}",
                    )
                    game_state["gameStart"] = False
                    await self.game_finish(game_state, winnerId)
                    return

                if game_state["gameStart"]:
                    await socket_send(game_state["render_data"], "score", game_id)
                    self.reset_ball(game_state, ball)

        await self.broadcast_game_state(game_state)

    async def check_paddle_collision(self, ball, paddle, game_state):
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
            game_state["current_rally"] += 1
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

    async def check_powerball(self, game_state, data):
        game_id = game_state["game_id"]
        player = (
            game_state["render_data"]["playerOne"]
            if not data.get("who")
            else game_state["render_data"]["playerTwo"]
        )

        is_collision = [
            ball
            for ball in game_state["render_data"]["balls"]
            if self.is_in_range(int(ball.position["x"]), int(player["x"]), 10)
            and self.is_in_range(int(ball.position["z"]), int(player["z"]), 10)
        ]
        if len(is_collision) == 1:
            self.set_ball_velocity(game_state, is_collision[0], 2)
            logger.info(f"Collision: {is_collision[0].position}")
            await socket_send(
                game_state["render_data"],
                "effect",
                game_id,
                is_collision[0].position,
            )

    def is_in_range(self, number, target, range):
        return abs(number - target) <= range

    def reset_ball(self, game_state, ball):
        ball.position = {"x": 0, "y": 5, "z": 0}
        ball.powerCounter = 0
        self.set_ball_velocity(game_state, ball)

    def reset_all_balls(self, game_state):
        for ball in self.game_state["balls"]:
            self.reset_ball(game_state, ball)

    def handle_ai_input(self, game_state, key, pressed):
        player = game_state["render_data"]["playerTwo"]
        if key == "A" and pressed:
            player["x"] -= Game.MOVE_SPEED.value
        elif key == "D" and pressed:
            player["x"] += Game.MOVE_SPEED.value

        player["x"] = max(
            -Game.GAME_WIDTH.value / 2 + 10,
            min(Game.GAME_WIDTH.value / 2 - 10, player["x"]),
        )

    async def broadcast_game_state(self, game_state):
        # logger.info("Broadcasting game state...")
        game_id = game_state["game_id"]
        await socket_send(game_state["render_data"], "gameState", game_id)

    async def handle_player_input(self, game_state, player_id, key, pressed):
        logger.info(f"player_id: {player_id}")
        logger.info(f"user1: {game_state['playerOneId']}")
        logger.info(f"user2: {game_state['playerTwoId']}")

        # logger.info(f"key???: {key}")
        await game_state["key_state_lock"].acquire()
        if player_id == "ai":
            # AI 플레이어의 입력 처리
            logger.info(f"AI key state: {game_state['two_keystate']}")
            self.handle_ai_input(game_state, key, pressed)
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

    async def paddle_loop(self, game_state):
        playerOne = game_state["render_data"]["playerOne"]
        oneName = game_state["render_data"]["oneName"]
        playerTwo = game_state["render_data"]["playerTwo"]
        twoName = game_state["render_data"]["twoName"]
        await self.process_paddle_move(
            game_state, oneName, playerOne, game_state["one_keystate"]
        )
        await self.process_paddle_move(
            game_state, twoName, playerTwo, game_state["two_keystate"]
        )

    async def process_paddle_move(self, game_state, playerName, player, key):
        if playerName == "ai":
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

    async def game_finish(self, game_state, winnerId):
        await save_game_history(game_state, winnerId)
        self.game_state.delete_game_state(game_state["game_id"])
        task_list = gameid_to_task[game_state["game_id"]]
        if (
            game_state["is_single_player"] == True
            and await delete_game(game_state["game_id"]) == False
        ):
            logger.error("Failed to delete game")
        for task in task_list:
            task.cancel()


@sync_to_async
def save_game_history(game_state, winnerId):
    game_id = game_state["game_id"]
    longest_rally = max(game_state["rallies"])
    average_rally = sum(game_state["rallies"]) / len(game_state["rallies"])
    game = GameHistory.objects.get(id=game_id)
    winner = game.user1 if game.user1.id == winnerId else game.user2
    # Save game history
    game.winner = winner
    game.ended_at = timezone.now()
    game.user1_score = game_state["render_data"]["score"]["playerOne"]
    game.user2_score = game_state["render_data"]["score"]["playerTwo"]
    game.longest_rally = longest_rally
    game.average_rally = average_rally
    game.save()
