from asgiref.sync import sync_to_async
from ingame.models import OneVersusOneGame
from pingpong_history.models import PingPongHistory
import logging

logger = logging.getLogger("django")


@sync_to_async
def get_game_users(game_id):
    game = OneVersusOneGame.objects.get(game_id=game_id)
    return game.user_1, game.user_2


@sync_to_async
def delete_game(game_id):
    try:
        game = OneVersusOneGame.objects.get(game_id=game_id)
        logger.info(f"1v1 game: {game}")
        game.delete()
        return True
    except OneVersusOneGame.DoesNotExist:
        return False
