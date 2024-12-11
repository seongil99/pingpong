from django.urls import path
from .consumers import OnlineStatusConsumer

websocket_urlpatterns = [
    path("online-status/", OnlineStatusConsumer.as_asgi()),
]
