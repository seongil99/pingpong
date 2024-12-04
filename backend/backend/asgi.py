"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from backend.GameIO import GameIO
from backend.sio import sio
import socketio

import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
logger = logging.getLogger("django")

sio.register_namespace(GameIO("/api/game"))

django_asgi_app = get_asgi_application()

game_app = socketio.ASGIApp(sio, socketio_path="/api/game/socket.io")

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Handle HTTP traffic
        "websocket": AuthMiddlewareStack(game_app),
        # "websocket": URLRouter(
        #     [  # WebSocket routing
        #         path("api/game/", game_app),
        #         path("api/game/socket.io/", game_app),
        #     ]
        # ),
    }
)
