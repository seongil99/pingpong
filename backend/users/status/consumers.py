from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils.timezone import now
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Mark user as online
            await self.set_user_online_status(True)
            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Mark user as offline
            await self.set_user_online_status(False)

    async def set_user_online_status(self, is_online):
        self.user.is_online = is_online
        self.user.last_seen = now()
        await database_sync_to_async(self.user.save)()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "heartbeat":
            # logger.info(f"Heartbeat received from {self.user.email}")
            pass
