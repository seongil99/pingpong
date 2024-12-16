from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from django.test import TransactionTestCase, override_settings

from tournament.consumers import TournamentGameProcessConsumer
from tournament.models import Tournament, TournamentParticipant, TournamentMatchParticipants

User = get_user_model()

test_channel_layers = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

application = AuthMiddlewareStack(
    URLRouter([
        path("ws/tournament/game/<int:tournament_id>/", TournamentGameProcessConsumer.as_asgi()),
    ])
)


class TournamentGameProcessConsumerTest(TransactionTestCase):
    def setUp(self):
        self.override_settings = override_settings(CHANNEL_LAYERS=test_channel_layers)
        self.override_settings.enable()

        # 유저 4명 생성
        self.user1 = User.objects.create_user(username="user1", email="user1@test.com", password="pass1")
        self.user2 = User.objects.create_user(username="user2", email="user2@test.com", password="pass2")
        self.user3 = User.objects.create_user(username="user3", email="user3@test.com", password="pass3")
        self.user4 = User.objects.create_user(username="user4", email="user4@test.com", password="pass4")

        # 토너먼트 생성
        self.tournament = Tournament.objects.create(status="pending", current_round=0)
        TournamentParticipant.objects.create(user=self.user1, tournament=self.tournament)
        TournamentParticipant.objects.create(user=self.user2, tournament=self.tournament)
        TournamentParticipant.objects.create(user=self.user3, tournament=self.tournament)
        TournamentParticipant.objects.create(user=self.user4, tournament=self.tournament)

        # matchparticipants 모델에 정보 저장 (가정)
        # 실 구현에 맞게 수정 필요
        # 이 모델은 토너먼트에 참가한 user1, user2, user3, user4를 묶어놓은 상태라고 가정
        TournamentMatchParticipants.objects.create(
            tournament=self.tournament,
            user1=self.user1,
            user2=self.user2,
            user3=self.user3,
            user4=self.user4
        )

    def tearDown(self):
        self.override_settings.disable()

    async def test_user_connect_and_ready(self):
        communicator1 = WebsocketCommunicator(application, f"/ws/tournament/game/{self.tournament.tournament_id}/")
        communicator1.scope["user"] = self.user1
        connected, subprotocol = await communicator1.connect()
        assert connected

        # ready 메시지 전송
        await communicator1.send_json_to({"type": "ready"})

        # consumer에서 ready 처리 -> 아직 모두 준비 안 되었으므로 user_ready 이벤트 발생
        response = await communicator1.receive_json_from()
        assert response["type"] == "user_ready"
        assert response["user"] == self.user1.username
        assert response["ready_count"] == 1

        await communicator1.disconnect()

    async def test_all_users_ready_starts_game(self):
        # 4명 모두 접속하고 ready 메시지를 보낸 후 game start 메시지 확인
        communicators = []
        for user in [self.user1, self.user2, self.user3]:
            comm = WebsocketCommunicator(application, f"/ws/tournament/game/{self.tournament.tournament_id}/")
            comm.scope["user"] = user
            connected, subprotocol = await comm.connect()
            assert connected
            await comm.send_json_to({"type": "ready"})
            communicators.append(comm)
            for c in communicators:
                response = await c.receive_json_from()
                assert response["type"] == "user_ready"
                assert response["user"] == user.username
                assert response["ready_count"] == len(communicators)

        # 4명 모두 접속하고 ready 메시지를 보낸 후 game start 메시지 확인
        comm = WebsocketCommunicator(application, f"/ws/tournament/game/{self.tournament.tournament_id}/")
        comm.scope["user"] = self.user4
        connected, subprotocol = await comm.connect()
        communicators.append(comm)
        assert connected
        await comm.send_json_to({"type": "ready"})

        response1 = await communicators[0].receive_json_from()
        response2 = await communicators[1].receive_json_from()
        response3 = await communicators[2].receive_json_from()
        response4 = await communicators[3].receive_json_from()

        assert response1["type"] == "game_started"
        assert response2["type"] == "game_started"
        assert response3["type"] == "game_started"
        assert response4["type"] == "game_started"

        assert response1["opponent"] == self.user2.username
        assert response2["opponent"] == self.user1.username
        assert response3["opponent"] == self.user4.username
        assert response4["opponent"] == self.user3.username

        assert response1["tournament_id"] == self.tournament.tournament_id
        assert response2["tournament_id"] == self.tournament.tournament_id
        assert response3["tournament_id"] == self.tournament.tournament_id
        assert response4["tournament_id"] == self.tournament.tournament_id

        assert response1["game_id"] == response2["game_id"]
        assert response3["game_id"] == response4["game_id"]

        tournament_status = await sync_to_async(lambda: Tournament.objects.get(pk=self.tournament.pk).status)()
        assert tournament_status == "ongoing"

        for user in [self.user1, self.user2, self.user3, self.user4]:
            is_ready = await sync_to_async(
                lambda: TournamentParticipant.objects.get(user=user, tournament=self.tournament).is_ready)()
            assert not is_ready

        for comm in communicators:
            await comm.disconnect()

    async def test_final_round_winner(self):
        communicators = []
        for user in [self.user1, self.user2, self.user3]:
            comm = WebsocketCommunicator(application, f"/ws/tournament/game/{self.tournament.tournament_id}/")
            comm.scope["user"] = user
            connected, subprotocol = await comm.connect()
            assert connected
            await comm.send_json_to({"type": "ready"})
            communicators.append(comm)
            for c in communicators:
                response = await c.receive_json_from()
                assert response["type"] == "user_ready"
                assert response["user"] == user.username
                assert response["ready_count"] == len(communicators)

        # 4명 모두 접속하고 ready 메시지를 보낸 후 game start 메시지 확인
        comm = WebsocketCommunicator(application, f"/ws/tournament/game/{self.tournament.tournament_id}/")
        comm.scope["user"] = self.user4
        connected, subprotocol = await comm.connect()
        communicators.append(comm)
        assert connected
        await comm.send_json_to({"type": "ready"})

        response1 = await communicators[0].receive_json_from()
        response2 = await communicators[1].receive_json_from()
        response3 = await communicators[2].receive_json_from()
        response4 = await communicators[3].receive_json_from()

        assert response1["type"] == "game_started"
        assert response2["type"] == "game_started"
        assert response3["type"] == "game_started"
        assert response4["type"] == "game_started"

        assert response1["opponent"] == self.user2.username
        assert response2["opponent"] == self.user1.username
        assert response3["opponent"] == self.user4.username
        assert response4["opponent"] == self.user3.username

        assert response1["tournament_id"] == self.tournament.tournament_id
        assert response2["tournament_id"] == self.tournament.tournament_id
        assert response3["tournament_id"] == self.tournament.tournament_id
        assert response4["tournament_id"] == self.tournament.tournament_id

        assert response1["game_id"] == response2["game_id"]
        assert response3["game_id"] == response4["game_id"]

        tournament_status = await sync_to_async(lambda: Tournament.objects.get(pk=self.tournament.pk).status)()
        assert tournament_status == "ongoing"

        for user in [self.user1, self.user2, self.user3, self.user4]:
            is_ready = await sync_to_async(
                lambda: TournamentParticipant.objects.get(user=user, tournament=self.tournament).is_ready)()
            assert not is_ready

        # user1, user3 승리
        await Tournament.objects.filter(pk=self.tournament.pk).aupdate(round_1_winner=self.user1,
                                                                       round_2_winner=self.user3)

        await TournamentParticipant.objects.filter(user=self.user2, tournament=self.tournament).adelete()
        await TournamentParticipant.objects.filter(user=self.user4, tournament=self.tournament).adelete()

        communicators = [communicators[0], communicators[2]]

        # user1, user3 승리로 인한 final round 시작
        for comm in communicators[:1]:
            await comm.send_json_to({"type": "ready"})
            for c in communicators:
                response = await c.receive_json_from()
                assert response["type"] == "user_ready"

        await communicators[1].send_json_to({"type": "ready"})

        response1 = await communicators[0].receive_json_from()
        response2 = await communicators[1].receive_json_from()

        assert response1["type"] == "game_started"
        assert response2["type"] == "game_started"

        assert response1["opponent"] == self.user3.username
        assert response2["opponent"] == self.user1.username

        assert response1["tournament_id"] == self.tournament.tournament_id
        assert response2["tournament_id"] == self.tournament.tournament_id

        assert response1["game_id"] == response2["game_id"]

        tournament_status = await sync_to_async(lambda: Tournament.objects.get(pk=self.tournament.pk).status)()
        assert tournament_status == "finished"

        for user in [self.user1, self.user3]:
            is_ready = await sync_to_async(
                lambda: TournamentParticipant.objects.get(user=user, tournament=self.tournament).is_ready)()
            assert not is_ready

        for comm in communicators:
            await comm.disconnect()
