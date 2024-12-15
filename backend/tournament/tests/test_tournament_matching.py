from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase, override_settings
from django.contrib.auth import get_user_model
from channels.routing import URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack

from tournament.consumers import TournamentMatchingConsumer
from tournament.models import Tournament, TournamentParticipant, TournamentGame, TournamentQueue

test_channel_layers = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

User = get_user_model()

application = AuthMiddlewareStack(
    URLRouter(
        [
            path("ws/tournament/matchmaking/", TournamentMatchingConsumer.as_asgi()),
        ]
    )
)


class TournamentMatchingConsumerTest(TransactionTestCase):
    def setUp(self):
        # 채널 레이어 설정 패치
        self.override_settings = override_settings(CHANNEL_LAYERS=test_channel_layers)
        self.override_settings.enable()
        # 동기적으로 사용자 생성
        self.user1 = User.objects.create_user(username="user1", password="password1", email="user1@test.com")
        self.user2 = User.objects.create_user(username="user2", password="password2", email="user2@test.com")
        self.user3 = User.objects.create_user(username="user3", password="password3", email="user3@test.com")
        self.user4 = User.objects.create_user(username="user4", password="password4", email="user4@test.com")

    def tearDown(self):
        # 패치 해제
        self.override_settings.disable()

    async def test_matchmaking_success(self):
        # 유저 1 웹소켓 연결
        communicator1 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        # 유저 1 매칭 요청
        await communicator1.send_json_to({"type": "request_match"})

        # 유저 1이 첫 번째 메시지 수신 (match_waiting)
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_waiting")
        self.assertEqual(response1["count"], 1)

        # 유저 2 웹소켓 연결
        communicator2 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator2.scope["user"] = self.user2
        connected2, subprotocol = await communicator2.connect()
        self.assertTrue(connected2)

        # 유저 2 매칭 요청
        await communicator2.send_json_to({"type": "request_match"})

        # 유저 2가 첫 번째 메시지 수신 (match_waiting)
        response2 = await communicator2.receive_json_from()
        self.assertEqual(response2["type"], "match_waiting")
        self.assertEqual(response2["count"], 2)

        # 유저 3 웹소켓 연결
        communicator3 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator3.scope["user"] = self.user3
        connected3, subprotocol = await communicator3.connect()
        self.assertTrue(connected3)

        # 유저 3 매칭 요청
        await communicator3.send_json_to({"type": "request_match"})

        # 유저 3이 첫 번째 메시지 수신 (match_waiting)
        response3 = await communicator3.receive_json_from()
        self.assertEqual(response3["type"], "match_waiting")
        self.assertEqual(response3["count"], 3)

        # 유저 3 매칭 취소 요청
        await communicator3.send_json_to({"type": "cancel_match"})
        response3 = await communicator3.receive_json_from()
        self.assertEqual(response3["type"], "match_canceled")
        queue_count = await self.get_queue_count()
        self.assertEqual(queue_count, 2)

        # 유저 3 다시 웹소켓 연결
        communicator3 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator3.scope["user"] = self.user3
        connected3, subprotocol = await communicator3.connect()
        self.assertTrue(connected3)

        # 유저 3 다시 매칭 요청
        await communicator3.send_json_to({"type": "request_match"})
        response3 = await communicator3.receive_json_from()
        self.assertEqual(response3["type"], "match_waiting")
        self.assertEqual(response3["count"], 3)

        # 유저 4 웹소켓 연결
        communicator4 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator4.scope["user"] = self.user4
        connected4, subprotocol = await communicator4.connect()
        self.assertTrue(connected4)

        # 유저 4 매칭 요청
        await communicator4.send_json_to({"type": "request_match"})

        # 모든 유저가 두 번째 메시지 수신 (match_found)
        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()
        response3 = await communicator3.receive_json_from()
        response4 = await communicator4.receive_json_from()

        self.assertEqual(response1["type"], "match_found")
        self.assertEqual(response2["type"], "match_found")
        self.assertEqual(response3["type"], "match_found")
        self.assertEqual(response4["type"], "match_found")

        self.assertEqual(response1["opponents"], [self.user2.username, self.user3.username, self.user4.username])
        self.assertEqual(response2["opponents"], [self.user1.username, self.user3.username, self.user4.username])
        self.assertEqual(response3["opponents"], [self.user1.username, self.user2.username, self.user4.username])
        self.assertEqual(response4["opponents"], [self.user1.username, self.user2.username, self.user3.username])

        self.assertIsNotNone(response1["tournament_id"])
        self.assertIsNotNone(response2["tournament_id"])
        self.assertIsNotNone(response3["tournament_id"])
        self.assertIsNotNone(response4["tournament_id"])

        # 토너먼트 확인
        tournament_id = response1["tournament_id"]
        tournament = await self.get_tournament(tournament_id)
        self.assertEqual(tournament.status, "pending")
        self.assertEqual(tournament.current_round, 0)
        self.assertIsNotNone(tournament.created_at)

        # 통신 종료
        await communicator1.disconnect()
        await communicator2.disconnect()
        await communicator3.disconnect()
        await communicator4.disconnect()

    async def test_matchmaking_waiting(self):
        # 동일하게 테스트 메서드 수정
        communicator1 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        await communicator1.send_json_to({"type": "request_match"})

        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_waiting")
        self.assertEqual(response1["count"], 1)

        await communicator1.disconnect()

    async def test_matchmaking_cancel(self):
        communicator1 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        await communicator1.send_json_to({"type": "request_match"})

        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_waiting")

        await communicator1.send_json_to({"type": "cancel_match"})

        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_canceled")
        queue_count = await self.get_queue_count()
        self.assertEqual(queue_count, 0)

        await communicator1.disconnect()

    @database_sync_to_async
    def get_queue_count(self):
        return TournamentQueue.objects.count()

    @database_sync_to_async
    def get_tournament(self, tournament_id):
        return Tournament.objects.get(tournament_id=tournament_id)
