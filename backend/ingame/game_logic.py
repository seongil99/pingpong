import environ
import math
import random
import threading
import time
import asyncio

from .enums import Game

env = environ.Env()
# PORT = env("INGAME_PORT") | 3000
PORT = 3000


async def set_interval(func, interval):
    while True:
        start_time = time.perf_counter()
        func()
        elapsed_time = (
            time.perf_counter() - start_time
        ) * 1_000_000  # Convert to microseconds
        print(f"Elapsed time: {elapsed_time:.2f} microseconds")
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
        return math.sqrt(self.x**2 + self.y**2 + self.z**2) ** 0.5

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
    def __init__(self, multiOption=False, ballCount=1):
        # In-memory store for game states
        self.game_id = self.generate_game_id()
        self.game_state = {
            "oneName": "sabyun",
            "twoName": "ai",
            "playerOne": {"x": 0, "y": 6, "z": 100},
            "playerTwo": {"x": 0, "y": 6, "z": -100},
            "balls": [],
            "score": {"playerOne": 0, "playerTwo": 0},
        }

        for i in range(0, ballCount):
            self.game_state["balls"].append(Ball(i))

        self.is_single_player = True if multiOption else {"A": False, "B": False}
        self.gameStart = False
        self.clients = {}

        self.save_game_state(self.game_id, self.game_state)

    def save_game_state(self, game_id, state):
        """Save the entire game state."""
        self.game_states[game_id] = state

    def load_game_state(self, game_id):
        """Load the game state."""
        return self.game_states.get(game_id)

    def update_game_state(self, game_id, updates):
        """Update parts of the game state."""
        if game_id in self.game_states:
            self.game_states[game_id].update(updates)
        else:
            raise KeyError(f"Game ID {game_id} not found.")

    def delete_game_state(self, game_id):
        """Delete the game state after the game ends."""
        if game_id in self.game_states:
            del self.game_states[game_id]
        else:
            raise KeyError(f"Game ID {game_id} not found.")

    def generate_game_id(self):
        return len(self.game_states) + 1


class PingPongServer:
    def __init__(self):
        self.game_state = InMemoryGameState(False, 1)
        self.gameId = self.game_state.game_id
        asyncio.run(set_interval(self.updatePhysics, Game.PHYSICS_INTERVAL.value))
        if self.is_single_player != True:
            asyncio.run(set_interval(self.update_ai, Game.AI_INTERVAL.value))

    def get_game_state(self):
        return self.game_state

    def addBall(self) -> None:
        ballNum = len(self.game_state["balls"])
        ball = Ball(ballNum)
        self.game_state["balls"].append(ball)
        self.setBallVelocity(ball, 1, True)

    def setBallVelocity(self, ball, powerUp=1, strat=False):
        MAX_ANGLE = math.pi / 6
        ANGLE = (random.random() * 2 - 1) * MAX_ANGLE
        direction = 1 if ball.summon_direction else -1
        if strat:
            direction = 1 if len(self.game_state["balls"]) == 1 else -1
        powerUp = 1 if ball.powerCounter > 1 else powerUp
        ball.powerCounter = 1 if powerUp == 2 else 0
        vx = math.sin(ANGLE) * Game.CONST_BALL_SPEED.value * powerUp
        vz = math.cos(ANGLE) * Game.CONST_BALL_SPEED.value * powerUp * direction
        ball.velocity = Vec3(vx, 0, vz)

    def update_ai(self):
        ball_position = self.game_state["balls"]
        target = 0
        if len(ball_position) != 1:
            target = min(
                range(len(ball_position)),
                key=lambda i: ball_position[i]["position"]["z"],
            )

        if (
            ball_position[target]["position"]["x"]
            < ball_position[target]["position"]["z"]
        ):
            return  # ball is coming towards the player

        if (
            ball_position[target]["position"]["z"] > 0
            or random.randint(0, 99) < self.AI_RATE
        ):
            return  # ball is over half, or AI decides to not act based on AI_RATE

        if ball_position[target]["position"]["x"] < self.game_state["playerTwo"]["x"]:
            if self.game_state.is_single_player["B"]:
                self.game_state.is_single_player["B"] = False
            if not self.game_state.is_single_player["A"]:
                self.game_state.is_single_player["A"] = True
            self.handle_player_input("ai", "A", self.game_state.is_single_player["A"])
        else:
            if self.game_state.is_single_player["A"]:
                self.game_state.is_single_player["A"] = False
            if not self.game_state.is_single_player["B"]:
                self.game_state.is_single_player["B"] = True
            self.handle_player_input("ai", "D", self.game_state.is_single_player["B"])

    def update_physics(self):
        if not self.gameStart:
            return

        for ball in self.gameState["balls"]:
            # Update ball position
            ball.position["x"] += ball.velocity["x"] * (1 / 60)
            ball.position["y"] += ball.velocity["y"] * (1 / 60)
            ball.position["z"] += ball.velocity["z"] * (1 / 60)

            # Check paddle collisions
            self.check_paddle_collision(ball, self.gameState["playerOne"])
            self.check_paddle_collision(ball, self.gameState["playerTwo"])

            # Check wall collisions
            if abs(ball.position["x"]) > Game.GAME_WIDTH.value / 2 - 2:
                ball.velocity["x"] *= -1
                self.socket_send("sound", "ballToWall")

            # Check scoring
            if (
                abs(ball.position["z"]) > Game.GAME_LENGTH.value / 2
                or ball.position["y"] < 0
                or ball.position["y"] > 20
            ):
                if ball.position["z"] > 0:
                    self.game_state["score"]["playerTwo"] += 1
                    ball.summon_direction = True
                else:
                    self.game_state["score"]["playerOne"] += 1
                    ball.summon_direction = False

                # Check if someone has won the set
                if (
                    self.game_state["score"]["playerOne"] > Game.GAME_SET_SCORE.value
                    or self.game_state["score"]["playerTwo"] > Game.GAME_SET_SCORE.value
                ):
                    print("end!!")
                    winner = (
                        self.game_state["oneName"]
                        if self.game_state["score"]["playerOne"]
                        > self.game_state["score"]["playerTwo"]
                        else self.game_state["twoName"]
                    )
                    self.socket_send("gameEnd", f"Winner is {winner}")
                    self.gameStart = False

                if self.gameStart:
                    self.socket_send("score")
                    self.reset_ball(ball)

        self.broadcast_game_state()

    def check_paddle_collision(self, ball, paddle):
        # 1. Find the closest point on the paddle to the ball
        closest_point = {
            "x": max(
                paddle["x"] - Game.PADDLE_WIDTH.value / 2,
                min(ball["position"]["x"], paddle["x"] + Game.PADDLE_WIDTH.value / 2),
            ),
            "y": max(
                paddle["y"] - Game.PADDLE_HEIGHT.value / 2,
                min(ball["position"]["y"], paddle["y"] + Game.PADDLE_HEIGHT.value / 2),
            ),
            "z": max(
                paddle["z"] - Game.PADDLE_DEPTH.value / 2,
                min(ball["position"]["z"], paddle["z"] + Game.PADDLE_DEPTH.value / 2),
            ),
        }

        # 2. Calculate the distance between the ball's center and the closest point on the paddle
        distance = math.sqrt(
            (ball["position"]["x"] - closest_point["x"]) ** 2
            + (ball["position"]["y"] - closest_point["y"]) ** 2
            + (ball["position"]["z"] - closest_point["z"]) ** 2
        )

        # 3. If the distance is less than or equal to the ball's radius, it's a collision
        if distance <= Game.BALL_SIZE.value:
            self.socket_send("sound", "ballToWall")
            hit_point_diff = ball["position"]["x"] - paddle["x"]
            max_bounce_angle = math.pi / 3
            bounce_angle = (hit_point_diff / 10) * max_bounce_angle

            # Calculate speed of the ball
            speed = Vec3(
                ball["velocity"]["x"], ball["velocity"]["y"], ball["velocity"]["z"]
            ).length()
            direction = -1 if ball["position"]["z"] < paddle["z"] else 1

            # Update ball's velocity after the collision
            ball["velocity"]["x"] = math.sin(bounce_angle) * speed
            ball["velocity"]["z"] = math.cos(bounce_angle) * speed * direction
            ball["velocity"]["y"] = min(ball["velocity"]["y"], 0)

    def is_in_range(self, number, target, range):
        return abs(number - target) <= range

    def reset_ball(self, ball):
        ball["position"] = {"x": 0, "y": 5, "z": 0}
        ball["power_counter"] = 0
        self.set_ball_velocity(ball)

    def reset_all_balls(self):
        for ball in self.game_state["balls"]:
            self.reset_ball(ball)

    def broadcast_game_state(self):
        self.socket_send("gameState")

    def set_ball_velocity(self, ball):
        # Placeholder for setting the ball's velocity
        # You would implement the logic to reset the ball's velocity here
        ball["velocity"] = {"x": 0, "y": 0, "z": 0}

    def handle_player_input(self, player_id, key, pressed):
        player = (
            self.game_state["playerTwo"]
            if player_id == "ai" or player_id == list(self.clients.keys())[1]
            else self.game_state["playerOne"]
        )
        move_speed = 2

        if key == "A" and pressed:
            player["x"] -= move_speed
        elif key == "D" and pressed:
            player["x"] += move_speed

        # Ensure player stays within boundaries
        player["x"] = max(
            -Game.GAME_WIDTH.value / 2 + 10,
            min(Game.GAME_WIDTH.value / 2 - 10, player["x"]),
        )

    async def socket_send(self, type, op=None):
        if type in ["gameStart", "gameState", "score"]:
            # Send the game state with type
            if not op:
                await self.sio.emit("data", {**self.game_state, "type": type})
            else:
                await op.emit("data", {**self.game_state, "type": type})

        elif type == "gameWait" and op:
            # Send the 'gameWait' type to a specific socket
            await op.emit("data", {"type": type})

        elif type == "secondPlayer":
            # Handle sending data to second player
            if not self.game_state.is_single_player:
                await self.sio.emit("data", {"type": type}, room=op)
            await self.socket_send("gameStart")

        elif not op:
            # If no 'op' socket is provided, send to all connected clients
            await self.sio.emit("data", {"type": type})

        elif type == "gameEnd":
            # Send 'gameEnd' data with additional text (op)
            await self.sio.emit("data", {"type": type, "txt": op})

        elif type == "sound":
            # Send sound data
            await self.sio.emit("data", {"type": type, "sound": op})

        elif type == "effect":
            # Send effect data
            await self.sio.emit("data", {"type": type, "effect": op})
