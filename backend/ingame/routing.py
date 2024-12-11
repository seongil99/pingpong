from django.urls import path
from .consumers import GameConsumer

websocket_urlpatterns = [
    path("game/", GameConsumer.as_asgi()),
]
