import random

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
from django.contrib.auth import get_user_model

from pingpong_history.models import PingPongHistory
from .models import Tournament, TournamentParticipant, TournamentGame, TournamentQueue, TournamentMatchParticipants
from ingame.utils import create_game_and_get_game_id

User = get_user_model()

import random
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db import transaction
from django.contrib.auth import get_user_model

from tournament.models import Tournament, TournamentParticipant, TournamentMatchParticipants, TournamentQueue

User = get_user_model()


class TournamentMatchingConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None
        self.current_tournament_id = None  # 추가: 현재 토너먼트 ID 추적용

    # ---------------------
    # Connection Handling
    # ---------------------
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated and not await self.is_user_duplicate():
            await self.accept()
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.current_tournament_id is not None:
            tournament_exists = await self.tournament_exists(self.current_tournament_id)
            if tournament_exists:
                multi_ball = await self.get_tournament_multi_ball(self.current_tournament_id)
                if multi_ball is None:
                    # 옵션 미설정 -> 토너먼트 삭제 및 강제 종료 로직
                    await self.delete_tournament_data(self.current_tournament_id)
                    await self.channel_layer.group_send(
                        f"tournament_{self.current_tournament_id}",
                        {
                            "type": "force_disconnect",
                        }
                    )
                    await self.close()
                    return
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.cancel_match()

    # ---------------------
    # Receive & Message Handling
    # ---------------------
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            data = await self.decode_json(text_data)
            await self.receive_json(data, **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    async def receive_json(self, content, **kwargs):
        msg_type = content.get("type")
        try:
            if msg_type == "request_match":
                await self.handle_request_match()
            elif msg_type == "cancel_match":
                await self.cancel_match()
            elif msg_type == "set_option":
                await self.handle_set_option(content)
            else:
                raise ValueError("Invalid message type")
        except Exception as e:
            await self.send_json({"type": "error", "message": str(e)})

    # ---------------------
    # Handlers
    # ---------------------
    async def handle_request_match(self):
        await self.add_to_queue()
        count = await self.get_queue_count()
        if count < 4:
            await self.send_json({"type": "match_waiting", "count": count})
        else:
            # 4명 추출
            players = await self.get_players_from_queue()
            random_val = random.Random().randint(0, 3)
            option_selector = players[random_val]

            await self.delete_users_from_queue(players)
            tournament_id = await self.create_and_get_tournament_id(players)
            await self.set_tournament_option_selector(tournament_id, option_selector)

            for p in players:
                group_name = f"user_{p.id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "match_found",
                        "opponents": [u.username for u in players if u != p],
                        "tournament_id": tournament_id,
                        "option_selector": option_selector == p,
                    }
                )

    async def handle_set_option(self, content):
        tournament_id = content["tournament_id"]
        multi_ball = content["multi_ball"]

        if isinstance(multi_ball, bool) and await self.can_user_set_tournament_option(tournament_id):
            multi_ball = await self.set_tournament_option(tournament_id, multi_ball)
            players = await self.get_tournament_players(tournament_id)
            for p in players:
                group_name = f"user_{p.id}"
                await self.channel_layer.group_send(
                    group_name,
                    {
                        "type": "set_option",
                        "tournament_id": tournament_id,
                        "multi_ball": multi_ball,
                    }
                )
        else:
            await self.send_json({
                "type": "error",
                "message": "You are not allowed to set options for this tournament"
            })

    # ---------------------
    # Events from group_send
    # ---------------------
    async def match_found(self, event):
        # match_found 이벤트 시 현재 토너먼트 ID를 저장하고
        # 해당 토너먼트 그룹에도 참가자를 추가
        self.current_tournament_id = event["tournament_id"]
        await self.channel_layer.group_add(f"tournament_{self.current_tournament_id}", self.channel_name)

        await self.send_json({
            "type": "match_found",
            "opponents": event["opponents"],
            "tournament_id": event["tournament_id"],
            "option_selector": event["option_selector"],
        })

    async def set_option(self, event):
        await self.send_json({
            "type": "set_option",
            "tournament_id": event["tournament_id"],
            "multi_ball": event["multi_ball"],
        })

    async def error(self, event):
        await self.send_json({"type": "error", "message": event["message"]})

    async def force_disconnect(self, event):
        # 토너먼트 중단시 모든 참가자 disconnect
        await self.send_json({"type": "force_disconnect"})
        await self.close()

    # ---------------------
    # Cancel match
    # ---------------------
    async def cancel_match(self):
        await self.remove_from_queue()
        await self.send_json({"type": "match_canceled"})
        await self.close()

    # ---------------------
    # Database / Utility Methods
    # ---------------------
    @database_sync_to_async
    def get_tournament_players(self, tournament_id):
        with transaction.atomic():
            participants = TournamentParticipant.objects.filter(tournament_id=tournament_id)
            return [p.user for p in participants]

    @database_sync_to_async
    def can_user_set_tournament_option(self, tournament_id):
        with transaction.atomic():
            try:
                tournament = Tournament.objects.get(tournament_id=tournament_id)
            except Tournament.DoesNotExist:
                return False
            return tournament.option_selector == self.user

    @database_sync_to_async
    def set_tournament_option(self, tournament_id, multi_ball: bool):
        with transaction.atomic():
            tournament = Tournament.objects.get(tournament_id=tournament_id)
            tournament.multi_ball = multi_ball
            tournament.save()
            return tournament.multi_ball

    @database_sync_to_async
    def set_tournament_option_selector(self, tournament_id, option_selector):
        with transaction.atomic():
            Tournament.objects.filter(tournament_id=tournament_id).update(option_selector=option_selector)

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
            return list(User.objects.filter(id__in=players_id))

    @database_sync_to_async
    def delete_users_from_queue(self, players):
        with transaction.atomic():
            TournamentQueue.objects.filter(user__in=players).delete()

    @database_sync_to_async
    def is_user_duplicate(self):
        return TournamentQueue.objects.filter(user=self.user).exists()

    @database_sync_to_async
    def get_tournament_multi_ball(self, tournament_id):
        with transaction.atomic():
            try:
                tournament = Tournament.objects.get(tournament_id=tournament_id)
                return tournament.multi_ball
            except Tournament.DoesNotExist:
                return None

    @database_sync_to_async
    def delete_tournament_data(self, tournament_id):
        with transaction.atomic():
            # 종속 객체 명시적 삭제
            TournamentParticipant.objects.filter(tournament_id=tournament_id).delete()
            TournamentMatchParticipants.objects.filter(tournament_id=tournament_id).delete()
            # 필요하다면 TournamentGame, PingPongHistory 등도 여기서 삭제
            Tournament.objects.filter(tournament_id=tournament_id).delete()

    @database_sync_to_async
    def tournament_exists(self, tournament_id):
        return Tournament.objects.filter(tournament_id=tournament_id).exists()


# 특정 유저의 채널 이름을 저장하는 딕셔너리
user_channel_name_map = {}


class TournamentGameProcessConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None
        self.user = None
        self.tournament_id = None

    # ---------------------
    # Connection Handling
    # ---------------------
    async def connect(self):
        self.user = self.scope["user"]
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]
        if self.user.is_authenticated and await self.is_user_participant():
            await self.accept()
            self.group_name = f"tournament_{self.tournament_id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            user_channel_name_map[self.user.id] = self.channel_name
        else:
            await self.close()

    async def disconnect(self, close_code):
        # 사용자 이탈 알림
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "user_left",
                "tournament_id": self.tournament_id,
                "user": self.user.username,
            }
        )
        # 이탈한 사용자의 준비 상태 해제
        await (TournamentParticipant.objects
               .filter(user=self.user, tournament_id=self.tournament_id)
               .aupdate(is_ready=False))
        # 채널 맵에서 제거
        if self.user.id in user_channel_name_map:
            del user_channel_name_map[self.user.id]
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.close()

    # ---------------------
    # Receive & Message Handling
    # ---------------------
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if text_data:
            await self.receive_json(await self.decode_json(text_data), **kwargs)
        else:
            raise ValueError("No text section for incoming WebSocket frame!")

    async def receive_json(self, content, **kwargs):
        try:
            msg_type = content.get("type")

            if msg_type == "ready":
                await self.handle_ready()
            else:
                raise ValueError("Invalid message type")

        except Exception as e:
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "error",
                    "message": str(e)
                }
            )

    async def handle_ready(self):
        await (TournamentParticipant.objects
               .filter(user=self.user, tournament_id=self.tournament_id)
               .aupdate(is_ready=True))
        is_all_ready = await self.check_all_ready()
        if is_all_ready:
            await self.start_game()
        else:
            ready_count = await TournamentParticipant.objects.filter(
                tournament_id=self.tournament_id, is_ready=True
            ).acount()
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "user_ready",
                    "user": self.user.username,
                    "ready_count": ready_count,
                }
            )

    # ---------------------
    # Helpers / Database Calls
    # ---------------------
    @database_sync_to_async
    def is_user_participant(self):
        return TournamentParticipant.objects.filter(user=self.user, tournament_id=self.tournament_id).exists()

    @database_sync_to_async
    def check_all_ready(self):
        return not TournamentParticipant.objects.filter(tournament_id=self.tournament_id, is_ready=False).exists()

    @database_sync_to_async
    def get_participants(self):
        participants = TournamentMatchParticipants.objects.get(tournament_id=self.tournament_id)
        return [participants.user1, participants.user2, participants.user3, participants.user4]

    @database_sync_to_async
    def get_tournament_winners(self):
        tournament = Tournament.objects.get(tournament_id=self.tournament_id)
        return [tournament.round_1_winner, tournament.round_2_winner]

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

    @database_sync_to_async
    def is_tournament_multi_ball(self):
        with transaction.atomic():
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)
            return tournament.multi_ball

    @database_sync_to_async
    def create_one_versus_one_game(self, game_id, user1, user2):
        from ingame.models import OneVersusOneGame
        with transaction.atomic():
            history = PingPongHistory.objects.get(id=game_id)
            game = OneVersusOneGame.objects.create(game_id=history, user_1=user1, user_2=user2)
            return game.game_id

    # ---------------------
    # Game Flow
    # ---------------------
    async def start_game(self):
        tournament = await Tournament.objects.aget(tournament_id=self.tournament_id)
        tournament_round = tournament.current_round
        # 라운드 진행 로직
        if tournament_round == 0:
            await self.start_first_round()
        else:
            await self.start_final_round()

    async def start_first_round(self):
        participants = await self.get_participants()
        user1, user2, user3, user4 = participants

        # 1라운드 게임들 생성
        await self.create_game(user1, user2, 1)
        await self.create_game(user3, user4, 2)

        # 상태 업데이트
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(current_round=2))
        await (TournamentParticipant.objects.filter(tournament_id=self.tournament_id).aupdate(is_ready=False))
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(status="ongoing"))

    async def start_final_round(self):
        round_1_winner, round_2_winner = await self.get_tournament_winners()
        await self.create_game(round_1_winner, round_2_winner, 3)
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(status="finished"))
        await (Tournament.objects.filter(tournament_id=self.tournament_id).aupdate(current_round=3))
        await (TournamentParticipant.objects.filter(tournament_id=self.tournament_id).aupdate(is_ready=False))

    async def create_game(self, user1, user2, round_num):
        multi_ball = await self.is_tournament_multi_ball()
        game_id = await create_game_and_get_game_id(user1, user2, multi_ball=multi_ball)

        await self.create_one_versus_one_game(game_id, user1, user2)
        await self.create_tournament_game(game_id, round_num, user1, user2)

        # 각 유저에게 game_started 알림
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

    # ---------------------
    # Utility Methods for Sending Messages
    # ---------------------
    async def send_message_to_user(self, user_id: int, message: dict):
        channel_name = user_channel_name_map.get(user_id)
        if channel_name:
            await self.channel_layer.send(channel_name, message)

    # ---------------------
    # Event Handlers
    # ---------------------
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

    async def error(self, event):
        await self.send_json({"type": "error", "message": event["message"]})
