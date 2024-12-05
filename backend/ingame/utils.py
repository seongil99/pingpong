from .models import OneVersusOneGame
from asgiref.sync import sync_to_async


@sync_to_async
def create_game_and_get_game_id(user_1, user_2):
    game = OneVersusOneGame.objects.create(user_1=user_1, user_2=user_2)
    return game.game_id
