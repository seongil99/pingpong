"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import logging
import os

import socketio
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.urls import path, re_path

from users.status.routing import websocket_urlpatterns as status_websocket_urlpatterns
from matchmaking.routing import (
    websocket_urlpatterns as matchmaking_websocket_urlpatterns,
)
from tournament.routing import websocket_urlpatterns as tournament_websocket_urlpatterns
from backend.GameIO import GameIO
from backend.sio import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
logger = logging.getLogger("django")

sio.register_namespace(GameIO("/api/game"))

django_asgi_app = get_asgi_application()

game_app = socketio.ASGIApp(sio, socketio_path="/api/game/socket.io")

websocket_urlpatterns = (
        status_websocket_urlpatterns
        + matchmaking_websocket_urlpatterns
        + tournament_websocket_urlpatterns
)

websocket_urlpatterns_with_auth = AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

game_app_with_auth = AuthMiddlewareStack(game_app)

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Handle HTTP traffic
        # "websocket": game_app_with_auth,
        "websocket": URLRouter(
            [  # WebSocket routing
                path("api/game/", game_app_with_auth),
                path("api/game/socket.io/", game_app_with_auth),
                re_path(r"^api/", websocket_urlpatterns_with_auth),
            ]
        ),
    }
)
