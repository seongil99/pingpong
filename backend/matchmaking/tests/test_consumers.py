from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from click import option
from django.test import TransactionTestCase, override_settings
from django.contrib.auth import get_user_model
from channels.routing import URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
from asgiref.sync import sync_to_async

from pingpong_history.models import PingPongHistory
from ..consumers import MatchmakingConsumer
from ..models import MatchRequest

test_channel_layers = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

User = get_user_model()

application = AuthMiddlewareStack(
    URLRouter(
        [
            path("ws/matchmaking/", MatchmakingConsumer.as_asgi()),
        ]
    )
)


class OneVersusOneMatchmakingConsumerTest(TransactionTestCase):
    def setUp(self):
        # 채널 레이어 설정 패치
        self.override_settings = override_settings(CHANNEL_LAYERS=test_channel_layers)
        self.override_settings.enable()
        # 동기적으로 사용자 생성
        self.user1 = User.objects.create_user(
            username="user1", password="password1", email="user1@test.com"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password2", email="user2@test.com"
        )

    def tearDown(self):
        # 패치 해제
        self.override_settings.disable()

    async def test_matchmaking_success(self):
        # 유저 1 웹소켓 연결
        communicator1 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        # 유저 1 매칭 요청
        await communicator1.send_json_to({"type": "request_match", "gamemode": "1v1"})

        # 유저 1이 첫 번째 메시지 수신 (waiting_for_match)
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "waiting_for_match")

        # 유저 2 웹소켓 연결
        communicator2 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator2.scope["user"] = self.user2
        connected2, subprotocol = await communicator2.connect()
        self.assertTrue(connected2)

        # 유저 2 매칭 요청
        await communicator2.send_json_to({"type": "request_match", "gamemode": "1v1"})

        # 유저 1이 두 번째 메시지 수신 (match_found)
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "match_found")
        self.assertEqual(response1["opponent_id"], self.user2.id)
        self.assertEqual(response1["opponent_username"], self.user2.username)

        # 유저 2가 매칭 결과를 받았는지 확인
        response2 = await communicator2.receive_json_from()
        self.assertEqual(response2["type"], "match_found")
        self.assertEqual(response2["opponent_id"], self.user1.id)
        self.assertEqual(response2["opponent_username"], self.user1.username)

        # 통신 종료
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_waiting_for_match(self):
        # 동일하게 테스트 메서드 수정
        communicator1 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        await communicator1.send_json_to({"type": "request_match", "gamemode": "1v1"})

        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "waiting_for_match")

        await communicator1.disconnect()

    async def test_cancel_match(self):
        communicator1 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, subprotocol = await communicator1.connect()
        self.assertTrue(connected1)

        await communicator1.send_json_to({"type": "request_match", "gamemode": "1v1"})

        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "waiting_for_match")

        await communicator1.send_json_to(
            {
                "type": "cancel_match",
            }
        )

        response2 = await communicator1.receive_json_from()
        self.assertEqual(response2["type"], "match_canceled")

        remaining_requests = await sync_to_async(
            MatchRequest.objects.filter(user=self.user1).count
        )()
        self.assertEqual(remaining_requests, 0)

        await communicator1.disconnect()

    async def test_set_option(self):
        # 유저1 접속 및 매칭 요청
        communicator1 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator1.scope["user"] = self.user1
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)
        await communicator1.send_json_to({"type": "request_match", "gamemode": "1v1"})
        response1 = await communicator1.receive_json_from()
        self.assertEqual(response1["type"], "waiting_for_match")

        # 유저2 접속 및 매칭 요청
        communicator2 = WebsocketCommunicator(application, "/ws/matchmaking/")
        communicator2.scope["user"] = self.user2
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)
        await communicator2.send_json_to({"type": "request_match", "gamemode": "1v1"})

        # 유저1 match_found 수신
        match_found_1 = await communicator1.receive_json_from()
        self.assertEqual(match_found_1["type"], "match_found")
        self.assertIn("game_id", match_found_1)
        game_id = match_found_1["game_id"]

        # 유저2 match_found 수신
        match_found_2 = await communicator2.receive_json_from()
        self.assertEqual(match_found_2["type"], "match_found")

        option_selector = await self.get_option_selector(game_id)
        option_selector_communicator = communicator1 if option_selector == self.user1 else communicator2

        # 유저1이 set_option 요청
        await option_selector_communicator.send_json_to(
            {
                "type": "set_option",
                "game_id": game_id,
                "multi_ball": True
            }
        )

        # 유저1 응답 수신(설정 성공)
        response_set_option_1 = await communicator1.receive_json_from()
        self.assertEqual(response_set_option_1["type"], "set_option")
        self.assertEqual(response_set_option_1["game_id"], game_id)
        self.assertTrue(response_set_option_1["multi_ball"])

        # 유저2가 set_option 알림 수신
        response_set_option_2 = await communicator2.receive_json_from()
        self.assertEqual(response_set_option_2["type"], "set_option")
        self.assertEqual(response_set_option_2["game_id"], game_id)
        self.assertTrue(response_set_option_2["multi_ball"])

        await communicator1.disconnect()
        await communicator2.disconnect()

    @database_sync_to_async
    def get_option_selector(self, game_id):
        history = PingPongHistory.objects.get(id=game_id)
        return history.option_selector
