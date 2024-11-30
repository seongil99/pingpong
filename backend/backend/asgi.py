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
from django.urls import path

from users.status.routing import websocket_urlpatterns as status_websocket_urlpatterns
from matchmaking.routing import websocket_urlpatterns as matchmaking_websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

websocket_urlpatterns = (
        status_websocket_urlpatterns
        + matchmaking_websocket_urlpatterns
)

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    # Add WebSocket routes here
                    path("api/", URLRouter(websocket_urlpatterns)),
                ]
            )
        ),
    }
)
