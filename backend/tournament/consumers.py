from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Tournament, TournamentParticipant, TournamentGame, TournamentQueue, TournamentMatchParticipants

User = get_user_model()


class TournamentMatchingConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
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
                await self.add_to_queue()

                # 대기열 인원 확인
                count = await self.get_queue_count()
                if count < 4:
                    # 아직 4명 미만이면 대기
                    await self.send_json(
                        {"type": "match_waiting", "count": count}
                    )
                else:
                    # 4명 달성 -> 4명 추출
                    players = await self.get_players_from_queue()
                    await self.delete_users_from_queue(players)
                    tournament_id = await self.create_and_get_tournament_id(players)

                    # 4명 모두에게 match_found 전송
                    for p in players:
                        group_name = f"user_{p.id}"
                        await self.channel_layer.group_send(
                            group_name,
                            {
                                "type": "match_found",
                                "opponents": [u.username for u in players if u != p],
                                "tournament_id": tournament_id,
                            }
                        )

            elif content.get("type") == "cancel_match":
                await self.cancel_match()
            else:
                raise ValueError("Invalid message type")
        except Exception as e:
            await self.send_json({"error": str(e)})

    async def match_found(self, event):
        await self.send_json({
            "type": "match_found",
            "opponents": event["opponents"],
            "tournament_id": event["tournament_id"],
        })

    async def cancel_match(self):
        await self.remove_from_queue()
        await self.send_json({"type": "match_canceled"})
        await self.close()

    @database_sync_to_async
    def add_to_queue(self):
        with transaction.atomic():
            TournamentQueue.objects.get_or_create(user=self.user)

    @database_sync_to_async
    def remove_from_queue(self):
        with transaction.atomic():
            TournamentQueue.objects.filter(user=self.user).delete()

    @database_sync_to_async
    def create_and_get_tournament_id(self, players):
        # 토너먼트를 생성하고 participants 추가
        # atomic 블럭 내에서 처리
        with transaction.atomic():
            tournament = Tournament.objects.create()
            for p in players:
                TournamentParticipant.objects.create(user=p, tournament=tournament)
            TournamentMatchParticipants.objects.create(
                tournament=tournament,
                user1=players[0],
                user2=players[1],
                user3=players[2],
                user4=players[3],
            )
            return tournament.tournament_id

    @database_sync_to_async
    def get_queue_count(self):
        return TournamentQueue.objects.count()

    @database_sync_to_async
    def get_players_from_queue(self):
        with transaction.atomic():
            players_id = TournamentQueue.objects.values_list("user", flat=True)[:4]
            players = list(User.objects.filter(id__in=players_id))
            return players

    @database_sync_to_async
    def delete_users_from_queue(self, players):
        with transaction.atomic():
            TournamentQueue.objects.filter(user__in=players).delete()
