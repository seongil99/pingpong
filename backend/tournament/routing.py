from django.urls import path
from .consumers import TournamentMatchingConsumer, TournamentGameProcessConsumer

websocket_urlpatterns = [
    path("ws/tournament/matchmaking/", TournamentMatchingConsumer.as_asgi()),
    path("ws/tournament/game/<int:tournament_id>/", TournamentGameProcessConsumer.as_asgi()),
]