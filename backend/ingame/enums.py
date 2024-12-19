import math
import random
from enum import Enum


class Game(Enum):
    GAME_WIDTH = 100
    GAME_LENGTH = 250
    CONST_BALL_SPEED = 50
    GAME_SET_SCORE = 5
    AI_RATE = 10
    BALL_SIZE = 5
    PADDLE_WIDTH = 20
    PADDLE_HEIGHT = 5
    PADDLE_DEPTH = 5
    MOVE_SPEED = 2
    AI_INTERVAL = 1 / 10
    PHYSICS_INTERVAL = 1 / 60
    PADDLE_INTERVAL = 1 / 30
    MAX_ANGLE = math.pi / 6
    


class GameMode(Enum):
    PVP = "PVP"
    PVE = "PVE"
    TOURNAMENT = "TOURNAMENT"


class KeyState(Enum):
    LEFT = "A"
    NONE = ""
    RIGHT = "D"
