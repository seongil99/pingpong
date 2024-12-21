from .models import OneVersusOneGame
from pingpong_history.models import PingPongHistory
from asgiref.sync import sync_to_async
from .enums import GameMode


#gamemode 추가 
@sync_to_async
def create_game_and_get_game_id(user_1, user_2, option_selector=None, tournament_id=None, multi_ball=None):
    history = PingPongHistory.objects.create(
        user1=user_1,
        user2=user_2,
        gamemode=GameMode.PVP.value,
        option_selector=option_selector,
        tournament_id=tournament_id,
        multi_ball=multi_ball,
    )
    return history.id
