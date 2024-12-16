from asgiref.sync import sync_to_async
from ingame.models import OneVersusOneGame
from pingpong_history.models import PingPongHistory
import logging

logger = logging.getLogger("django")


@sync_to_async
def get_game_users(game_id):
    game = OneVersusOneGame.objects.get(game_id=game_id)
    return game.user_1, game.user_2



