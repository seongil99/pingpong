import socketio
from django.test import TransactionTestCase, override_settings
from unittest.mock import patch, AsyncMock
from backend.GameIO import GameIO, user_to_socket, user_to_game, game_state_db
from users.models import User
from pingpong_history.models import PingPongHistory
from ingame.enums import GameMode

test_channel_layers = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


@override_settings(CHANNEL_LAYERS=test_channel_layers)
class TestGameIODisconnect(TransactionTestCase):
    def setUp(self):
        """Set up async test fixtures."""
        self.user = User.objects.create(
            username="testuser", password="password", email="a"
        )
        self.user2 = User.objects.create(
            username="testuser2", password="password", email="b"
        )
        self.sid = "test_sid"

    async def test_disconnect_removes_user_from_socket(self):
        user_to_socket[self.user.id] = self.sid
        game_io = GameIO("/test")

        with patch("backend.GameIO.sio.get_session", return_value={"user": self.user}):
            await game_io.on_disconnect(self.sid)

        self.assertNotIn(self.user.id, user_to_socket)

    async def test_disconnect_removes_user_from_game(self):
        game_id = "0"
        user_to_game[self.sid] = game_id
        game_io = GameIO("/test")

        with patch("backend.GameIO.sio.get_session", return_value={"user": self.user}):
            await game_io.on_disconnect(self.sid)

        self.assertNotIn(self.sid, user_to_game)

    async def test_disconnect_updates_game_state(self):
        game_id = "0"
        user_to_game[self.sid] = game_id
        game_state = {
            "clients": {self.sid: self.sid},
            "gameStart": True,
            "game_start_lock": AsyncMock(),
        }
        game_state_db.load_game_state = AsyncMock(return_value=game_state)
        await PingPongHistory.objects.acreate(
            id=game_id, gamemode=GameMode.PVP.value, user1=self.user, user2=self.user2
        )

        game_io = GameIO("/test")
        with patch("backend.GameIO.sio.get_session", return_value={"user": self.user}):
            await game_io.on_disconnect(self.sid)

        self.assertNotIn(self.sid, game_state["clients"])
        game_state["game_start_lock"].acquire.assert_called_once()
        game_state["game_start_lock"].release.assert_called_once()


@override_settings(REST_AUTH={"JWT_AUTH_COOKIE": "jwt-auth"})
class TestGameIO(TransactionTestCase):
    def setUp(self):
        """Set up async test fixtures."""
        self.user = User.objects.create(username="testuser", password="password")
        self.sid = "test_sid"

    async def test_check_authentication_success(self):
        token = "valid_token"
        environ = {"HTTP_COOKIE": f"jwt-auth={token}"}

        with patch(
            "backend.GameIO.TokenBackend.decode", return_value={"user_id": self.user.id}
        ), patch("backend.GameIO.sio.save_session", new_callable=AsyncMock):
            game_io = GameIO("/api/game")
            result = await game_io._check_authentication(environ, self.sid)
            self.assertTrue(result)

    async def test_check_authentication_failure_no_token(self):
        environ = {"HTTP_COOKIE": ""}
        game_io = GameIO("/test")
        result = await game_io._check_authentication(environ, self.sid)
        self.assertFalse(result)

    async def test_check_authentication_failure_invalid_token(self):
        environ = {"HTTP_COOKIE": "jwt-auth=invalid_token"}

        with patch(
            "backend.GameIO.TokenBackend.decode", side_effect=Exception("InvalidToken")
        ):
            game_io = GameIO("/test")
            result = await game_io._check_authentication(environ, self.sid)
            self.assertFalse(result)
