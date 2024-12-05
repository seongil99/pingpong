from channels.db import database_sync_to_async
from ingame.models import OneVersusOneGame

@database_sync_to_async
def get_game_users(game_id):
    game = OneVersusOneGame.objects.get(game_id=game_id)
    return game.user_1, game.user_2
