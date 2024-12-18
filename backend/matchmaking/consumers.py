import random

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction

from ingame.utils import create_game_and_get_game_id
from .models import MatchRequest
from pingpong_history.models import PingPongHistory

from logging import getLogger

logger = getLogger(__name__)


class MatchmakingConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated and not await self.is_duplicate_user(self.user.id):
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
                if await self.is_user_in_other_game(self.user.id):
                    await self.send_json(
                        {
                            "type": "error",
                            "message": "이미 게임 중입니다.",
                        }
                    )
                    return
                gamemode = content["gamemode"]
                opponent = await self.find_match(gamemode)
                if opponent:
                    random_val = random.Random().randint(0, 1)
                    option_selector = self.user
                    if random_val == 0:
                        option_selector = opponent
                    game_id = await create_game_and_get_game_id(self.user, opponent, option_selector)
                    # 매칭이 성사되었습니다.
                    await self.send_json(
                        {
                            "type": "match_found",
                            "opponent_id": opponent.id,
                            "opponent_username": opponent.username,
                            "game_id": game_id,
                            "option_selector": option_selector == self.user,
                        }
                    )
                    # 상대방에게도 매칭 결과를 전송합니다.
                    await self.notify_opponent(opponent, game_id, option_selector == opponent)
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
            elif content.get("type") == "set_option":
                game_id = content["game_id"]
                multiball_option = content["multi_ball"]
                if not await self.can_user_set_option(game_id):
                    await self.send_json(
                        {
                            "type": "error",
                            "message": "옵션을 선택할 수 없습니다.",
                        }
                    )
                    return
                multiball_option = await self.save_multi_ball(game_id, multiball_option)
                opponent_id = await self.get_opponent_id(game_id)
                await self.send_json(
                    {
                        "type": "set_option",
                        "game_id": game_id,
                        "multi_ball": multiball_option,
                    }
                )
                await self.channel_layer.group_send(
                    f"user_{opponent_id}",
                    {
                        "type": "set_option",
                        "game_id": game_id,
                        "multi_ball": multiball_option,
                    },
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

    async def notify_opponent(self, opponent, game_id, is_option_selector):
        group_name = f"user_{opponent.id}"
        await self.channel_layer.group_send(
            group_name,
            {
                "type": "match_found",
                "opponent_id": self.user.id,
                "opponent_username": self.user.username,
                "game_id": game_id,
                "option_selector": is_option_selector,
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

    async def set_option(self, event):
        # 게임 옵션을 수신하여 클라이언트로 전달
        await self.send_json(
            {
                "type": "set_option",
                "game_id": event["game_id"],
                "multi_ball": event["multi_ball"],
            }
        )

    @database_sync_to_async
    def is_duplicate_user(self, user_id):
        return MatchRequest.objects.filter(user_id=user_id).exists()

    @database_sync_to_async
    def can_user_set_option(self, game_id):
        with transaction.atomic():
            try:
                game = PingPongHistory.objects.select_for_update().get(id=game_id)
            except PingPongHistory.DoesNotExist:
                return False
            return game.option_selector == self.user

    @database_sync_to_async
    def is_user_in_other_game(self, user_id):
        from ingame.models import OneVersusOneGame
        return OneVersusOneGame.objects.filter(user_1_id=user_id).exists() or \
            OneVersusOneGame.objects.filter(user_2_id=user_id).exists()

    @database_sync_to_async
    def cancel_match(self):
        MatchRequest.objects.filter(user=self.user).delete()

    @database_sync_to_async
    def get_opponent_id(self, game_id):
        history = PingPongHistory.objects.get(id=game_id)
        if history.user1 == self.user:
            return history.user2.id
        else:
            return history.user1.id

    @database_sync_to_async
    def save_multi_ball(self, game_id, option):
        with transaction.atomic():
            history = PingPongHistory.objects.get(id=game_id)
            history.multi_ball = option
            history.save()
        return history.multi_ball
