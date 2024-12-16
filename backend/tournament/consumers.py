from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
from django.contrib.auth import get_user_model

from pingpong_history.models import PingPongHistory
from .models import Tournament, TournamentParticipant, TournamentGame, TournamentQueue, TournamentMatchParticipants
from ingame.utils import create_game_and_get_game_id

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


# 특정 유저의 채널 이름을 저장하는 딕셔너리
user_channel_name_map = {}


class TournamentGameProcessConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None
        self.tournament_id = None

    async def connect(self):
        self.user = self.scope["user"]
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]
        if (self.user.is_authenticated
                and await self.is_user_participant()):
            await self.accept()
            self.group_name = f"tournament_{self.tournament_id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            user_channel_name_map[self.user.id] = self.channel_name
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_left",
                "tournament_id": self.tournament_id,
                "user": self.user.username,
            }
        )
        await (TournamentParticipant.objects
               .filter(user=self.user, tournament_id=self.tournament_id)
               .aupdate(is_ready=False))
        del user_channel_name_map[self.user.id]
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            await self.receive_json(await self.decode_json(text_data), **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    async def receive_json(self, content, **kwargs):
        try:
            if content.get("type") == "ready":
                await (TournamentParticipant.objects
                       .filter(user=self.user, tournament_id=self.tournament_id)
                       .aupdate(is_ready=True))
                is_all_ready = await self.check_all_ready()
                if is_all_ready:
                    await self.start_game()
                else:
                    ready_count = await TournamentParticipant.objects.filter(tournament_id=self.tournament_id,
                                                                             is_ready=True).acount()
                    await self.channel_layer.group_send(
                        self.group_name,
                        {
                            "type": "user_ready",
                            "user": self.user.username,
                            "ready_count": ready_count,
                        }
                    )
            else:
                raise ValueError("Invalid message type")

        except Exception as e:
            await self.send_json({"error": str(e)})

    @database_sync_to_async
    def is_user_participant(self):
        return TournamentParticipant.objects.filter(user=self.user, tournament_id=self.tournament_id).exists()

    @database_sync_to_async
    def check_all_ready(self):
        return not TournamentParticipant.objects.filter(tournament_id=self.tournament_id, is_ready=False).exists()

    async def send_message_to_user(self, user_id: int, message: dict):
        channel_name = user_channel_name_map.get(user_id)
        if channel_name:
            await self.channel_layer.send(channel_name, message)

    async def start_game(self):
        tournament = await Tournament.objects.aget(tournament_id=self.tournament_id)
        tournament_round = tournament.current_round
        if tournament_round == 0:
            # 첫 라운드 시작
            await self.start_first_round()
        else:
            # 이후 라운드 시작
            await self.start_final_round()

    @database_sync_to_async
    def get_participants(self):
        participants = TournamentMatchParticipants.objects.get(tournament_id=self.tournament_id)
        return [participants.user1, participants.user2, participants.user3, participants.user4]

    async def start_first_round(self):
        # 첫 라운드 게임 생성
        participants = await self.get_participants()
        user1, user2, user3, user4 = participants
        await self.create_game(user1, user2, 1)
        await self.create_game(user3, user4, 2)
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(current_round=2))
        await (TournamentParticipant.objects.filter(tournament_id=self.tournament_id).aupdate(is_ready=False))
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(status="ongoing"))

    @database_sync_to_async
    def get_tournament_winners(self):
        tournament = Tournament.objects.get(tournament_id=self.tournament_id)
        return [tournament.round_1_winner, tournament.round_2_winner]

    async def start_final_round(self):
        round_1_winner, round_2_winner = await self.get_tournament_winners()
        await self.create_game(round_1_winner, round_2_winner, 3)
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(status="finished"))
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(current_round=3))
        await (TournamentParticipant.objects.filter(tournament_id=self.tournament_id).aupdate(is_ready=False))

    @database_sync_to_async
    def create_tournament_game(self, game_id, round_num, user1, user2):
        with transaction.atomic():
            pingpong_history = PingPongHistory.objects.get(id=game_id)
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)
            TournamentGame.objects.create(
                game_id=pingpong_history,
                tournament_id=tournament,
                tournament_round=round_num,
                user_1=user1,
                user_2=user2,
            )

    async def create_game(self, user1, user2, round_num):
        game_id = await create_game_and_get_game_id(user1, user2)
        await self.create_tournament_game(game_id, round_num, user1, user2)
        await self.send_message_to_user(user1.id,
                                        {"type": "game_started",
                                         "game_id": game_id,
                                         "tournament_id": self.tournament_id,
                                         "opponent": user2.username})
        await self.send_message_to_user(user2.id,
                                        {"type": "game_started",
                                         "game_id": game_id,
                                         "tournament_id": self.tournament_id,
                                         "opponent": user1.username})

    async def user_ready(self, event):
        await self.send_json({"type": "user_ready",
                              "user": event["user"],
                              "ready_count": event["ready_count"]})

    async def game_started(self, event):
        await self.send_json(
            {"type": "game_started",
             "game_id": event["game_id"],
             "tournament_id": event["tournament_id"],
             "opponent": event["opponent"]})

    async def user_left(self, event):
        await self.send_json({"type": "user_left",
                              "tournament_id": event["tournament_id"],
                              "user": event["user"]})
