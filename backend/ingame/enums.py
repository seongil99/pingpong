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
    AI_INTERVAL = 1 / 10
    PHYSICS_INTERVAL = 1 / 60
