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

    async def test_set_option_success(self):
        # 4명 모두 매칭하여 tournament_id 획득
        communicator1 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)
        await communicator1.send_json_to({"type": "request_match"})
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_waiting")

        communicator2 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator2.scope["user"] = self.user2
        connected2, subprotocol = await communicator2.connect()
        self.assertTrue(connected2)
        await communicator2.send_json_to({"type": "request_match"})
        response2 = await communicator2.receive_json_from()
        self.assertEqual(response2["type"], "match_waiting")

        communicator3 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator3.scope["user"] = self.user3
        connected3, subprotocol = await communicator3.connect()
        self.assertTrue(connected3)
        await communicator3.send_json_to({"type": "request_match"})
        response3 = await communicator3.receive_json_from()
        self.assertEqual(response3["type"], "match_waiting")

        communicator4 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator4.scope["user"] = self.user4
        connected4, subprotocol = await communicator4.connect()
        self.assertTrue(connected4)
        await communicator4.send_json_to({"type": "request_match"})

        # match_found 수신
        response1 = await communicator1.receive_json_from()
        response2 = await communicator2.receive_json_from()
        response3 = await communicator3.receive_json_from()
        response4 = await communicator4.receive_json_from()

        self.assertEqual(response1["type"], "match_found")
        self.assertEqual(response2["type"], "match_found")
        self.assertEqual(response3["type"], "match_found")
        self.assertEqual(response4["type"], "match_found")

        tournament_id = response1["tournament_id"]
        # option_selector 확인
        # 누군가가 option_selector == True로 반환되어야 함
        option_selector_user = None
        for resp, user in [(response1, self.user1), (response2, self.user2), (response3, self.user3),
                           (response4, self.user4)]:
            if resp["option_selector"] == True:
                option_selector_user = user
                break

        self.assertIsNotNone(option_selector_user, "No option_selector user found.")

        # option_selector 유저로부터 set_option 요청(예: multi_ball=True)
        # 다른 유저도 이를 받아야 함
        if option_selector_user == self.user1:
            selector_communicator = communicator1
        elif option_selector_user == self.user2:
            selector_communicator = communicator2
        elif option_selector_user == self.user3:
            selector_communicator = communicator3
        else:
            selector_communicator = communicator4

        await selector_communicator.send_json_to({
            "type": "set_option",
            "tournament_id": tournament_id,
            "multi_ball": True
        })

        # 모든 유저가 set_option 이벤트를 수신해야 함
        # option_selector 유저 본인
        set_option_resp_selector = await selector_communicator.receive_json_from()
        self.assertEqual(set_option_resp_selector["type"], "set_option")
        self.assertEqual(set_option_resp_selector["tournament_id"], tournament_id)
        self.assertTrue(set_option_resp_selector["multi_ball"])

        # 나머지 유저들
        others = [c for c in [communicator1, communicator2, communicator3, communicator4] if c != selector_communicator]
        for c in others:
            set_option_resp = await c.receive_json_from()
            self.assertEqual(set_option_resp["type"], "set_option")
            self.assertEqual(set_option_resp["tournament_id"], tournament_id)
            self.assertTrue(set_option_resp["multi_ball"])

        # 통신 종료
        await communicator1.disconnect()
        await communicator2.disconnect()
        await communicator3.disconnect()
        await communicator4.disconnect()

    async def test_force_disconnect_when_option_selector_leaves(self):
        # 1. 4명 매칭
        communicator1 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)
        await communicator1.send_json_to({"type": "request_match"})
        await communicator1.receive_json_from()  # match_waiting

        communicator2 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator2.scope["user"] = self.user2
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)
        await communicator2.send_json_to({"type": "request_match"})
        await communicator2.receive_json_from()  # match_waiting

        communicator3 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator3.scope["user"] = self.user3
        connected3, _ = await communicator3.connect()
        self.assertTrue(connected3)
        await communicator3.send_json_to({"type": "request_match"})
        await communicator3.receive_json_from()  # match_waiting

        communicator4 = WebsocketCommunicator(application, "/ws/tournament/matchmaking/")
        communicator4.scope["user"] = self.user4
        connected4, _ = await communicator4.connect()
        self.assertTrue(connected4)
        await communicator4.send_json_to({"type": "request_match"})

        resp1 = await communicator1.receive_json_from()  # match_found
        resp2 = await communicator2.receive_json_from()  # match_found
        resp3 = await communicator3.receive_json_from()  # match_found
        resp4 = await communicator4.receive_json_from()  # match_found

        self.assertEqual(resp1["type"], "match_found")
        self.assertEqual(resp2["type"], "match_found")
        self.assertEqual(resp3["type"], "match_found")
        self.assertEqual(resp4["type"], "match_found")

        tournament_id = resp1["tournament_id"]
        # 2. option_selector 찾기
        responses = [(resp1, self.user1, communicator1),
                     (resp2, self.user2, communicator2),
                     (resp3, self.user3, communicator3),
                     (resp4, self.user4, communicator4)]

        option_selector_user = None
        option_selector_communicator = None
        for r, u, c in responses:
            if r["option_selector"]:
                option_selector_user = u
                option_selector_communicator = c
                break

        self.assertIsNotNone(option_selector_user, "No option_selector found")

        # 3. 옵션 결정 전 option_selector 유저 접속 종료
        await option_selector_communicator.disconnect()

        # 4. 나머지 유저들(force_disconnect 수신 기대)
        # option_selector를 제외한 다른 커뮤니케이터에서 force_disconnect 수신
        others = [c for _, u, c in responses if u != option_selector_user]

        for c in others:
            # force_disconnect 이벤트 수신
            fd_msg = await c.receive_json_from()
            self.assertEqual(fd_msg["type"], "force_disconnect")

        # 5. 토너먼트 삭제 확인(토너먼트가 없어야 함)
        self.assertFalse(await self.tournament_exists(tournament_id))

    @database_sync_to_async
    def tournament_exists(self, tournament_id):
        return Tournament.objects.filter(tournament_id=tournament_id).exists()
