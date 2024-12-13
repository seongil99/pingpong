from django.urls import path
from channels.routing import URLRouter
from users.status.consumers import OnlineStatusConsumer

websocket_urlpatterns = [
    path("online-status/", OnlineStatusConsumer.as_asgi()),
]
