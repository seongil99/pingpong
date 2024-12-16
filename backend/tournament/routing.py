from django.urls import path
from .consumers import TournamentMatchingConsumer

websocket_urlpatterns = [
    path("ws/tournament/matchmaking/", TournamentMatchingConsumer.as_asgi()),
]