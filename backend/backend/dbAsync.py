import logging
from asgiref.sync import sync_to_async
from ingame.models import OneVersusOneGame
from pingpong_history.models import PingPongHistory
from tournament.models import TournamentGame

logger = logging.getLogger("django")


@sync_to_async
def get_game_users(game_id):
    """
    게임의 유저들을 가져오는 함수. 게임이 토너먼트 게임인지 1대1 게임인지 확인 후 가져옴. 게임이 이미 종료된 경우 예외 발생
    """
    game = PingPongHistory.objects.get(id=game_id)
    return game.user1, game.user2
