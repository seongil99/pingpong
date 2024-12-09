from .models import OneVersusOneGame
from pingpong_history.models import PingPongHistory
from asgiref.sync import sync_to_async
from .enums import GameMode


@sync_to_async
def create_game_and_get_game_id(user_1, user_2):
    history = PingPongHistory.objects.create(
        user1=user_1,
        user2=user_2,
        gamemode=GameMode.PVP.value,
    )
    OneVersusOneGame.objects.create(game_id=history, user_1=user_1, user_2=user_2)
    return history.id
