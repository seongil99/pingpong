import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction

from ingame.utils import create_game_and_get_game_id
from .models import MatchRequest


logger = logging.getLogger(__name__)


class MatchmakingConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
            # 사용자별 그룹에 가입
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.cancel_match()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            await self.receive_json(await self.decode_json(text_data), **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    async def receive_json(self, content, **kwargs):
        try:
            if content.get("type") == "request_match":
                gamemode = content["gamemode"]
                opponent = await self.find_match(gamemode)
                if opponent:
                    game_id = await create_game_and_get_game_id(self.user, opponent)
                    # 매칭이 성사되었습니다.
                    await self.send_json(
                        {
                            "type": "match_found",
                            "opponent_id": opponent.id,
                            "opponent_username": opponent.username,
                            "game_id": game_id,
                        }
                    )
                    # 상대방에게도 매칭 결과를 전송합니다.
                    await self.notify_opponent(opponent, game_id)
                else:
                    # 대기열에 추가되었습니다.
                    await self.send_json(
                        {
                            "type": "waiting_for_match",
                        }
                    )
            elif content.get("type") == "cancel_match":
                await self.cancel_match()
                await self.send_json(
                    {
                        "type": "match_canceled",
                    }
                )
        except Exception as e:
            await self.send_json(
                {
                    "type": "error",
                    "message": str(e),
                }
            )

    @database_sync_to_async
    def find_match(self, gamemode):
        with transaction.atomic():
            existing_request = (
                MatchRequest.objects.select_for_update()
                .filter(gamemode=gamemode)
                .exclude(user=self.user)
                .first()
            )

            if existing_request:
                opponent = existing_request.user
                existing_request.delete()
                return opponent
            else:
                MatchRequest.objects.create(user=self.user, gamemode=gamemode)
                return None

    async def notify_opponent(self, opponent, game_id):
        group_name = f"user_{opponent.id}"
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "match_found",
                "opponent_id": self.user.id,
                "opponent_username": self.user.username,
                "game_id": game_id,
            },
        )

    async def match_found(self, event):
        # 상대방으로부터 매칭 결과를 수신하여 클라이언트로 전달
        await self.send_json(
            {
                "type": "match_found",
                "opponent_id": event["opponent_id"],
                "opponent_username": event["opponent_username"],
                "game_id": event["game_id"],
            }
        )

    @database_sync_to_async
    def cancel_match(self):
        MatchRequest.objects.filter(user=self.user).delete()
