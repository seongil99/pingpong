import json
import logging
import socketio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.db import transaction

logger = logging.getLogger(__name__)


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    """
    온라인 상태 소켓 컨슈머
    """

    async def connect(self):
        """
        온라인 상태소켓 연결
        """
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            # Mark user as online
            await self._set_user_online_status(True)
            await self.accept()
            return
        logger.info("close called")
        await self.close(code=4001)

    async def disconnect(self, close_code):
        """
        온라인 상태소켓 연결 해제
        """
        logger.info("close code: %s", close_code)
        if self.user.is_authenticated:
            # Mark user as offline
            await self._set_user_online_status(False)

    @database_sync_to_async
    def _set_user_online_status(self, is_online):
        with transaction.atomic():
            self.user.refresh_from_db()
            self.user.is_online = is_online
            self.user.last_seen = now()
            self.user.save()

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "heartbeat":
            # logger.info(f"Heartbeat received from {self.user.email}")
            pass
