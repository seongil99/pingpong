import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.GameIO import GameIO

@pytest.mark.asyncio
async def test_check_authentication_success():
    game_io = GameIO('/api/game')
    environ = {"HTTP_COOKIE": "jwt-auth-token=valid_token;"}
    sid = "test_sid"

    with patch("backend.GameIO.settings") as mock_settings, \
         patch("backend.GameIO.SimpleCookie") as mock_SimpleCookie, \
         patch("backend.GameIO.TokenBackend") as mock_TokenBackend, \
         patch("backend.GameIO.User.objects.aget", new=AsyncMock()) as mock_aget, \
         patch("backend.GameIO.sio.save_session", new=AsyncMock()) as mock_save_session:
        
        mock_settings.REST_AUTH = {"JWT_AUTH_COOKIE": "jwt-auth-token"}
        mock_settings.SECRET_KEY = "secret_key"

        mock_cookie = MagicMock()
        mock_cookie.get.return_value = MagicMock(value='valid_token')
        mock_SimpleCookie.return_value = mock_cookie

        mock_token_backend_instance = mock_TokenBackend.return_value
        mock_token_backend_instance.decode.return_value = {"user_id": 1}

        mock_user = MagicMock()
        mock_aget.return_value = mock_user

        result = await game_io._check_authentication(environ, sid)

        assert result is True
        mock_save_session.assert_awaited_with(sid, {"user": mock_user}, namespace='/api/game')

@pytest.mark.asyncio
async def test_check_authentication_no_cookie():
    game_io = GameIO('/api/game')
    environ = {}
    sid = "test_sid"

    with patch("backend.GameIO.settings") as mock_settings:
        mock_settings.REST_AUTH = {"JWT_AUTH_COOKIE": "jwt-auth-token"}

        result = await game_io._check_authentication(environ, sid)

        assert result is False

@pytest.mark.asyncio
async def test_check_authentication_invalid_token():
    game_io = GameIO('/api/game')
    environ = {"HTTP_COOKIE": "jwt-auth-token=invalid_token;"}
    sid = "test_sid"

    with patch("backend.GameIO.settings") as mock_settings, \
         patch("backend.GameIO.SimpleCookie") as mock_SimpleCookie, \
         patch("backend.GameIO.TokenBackend") as mock_TokenBackend:
        
        mock_settings.REST_AUTH = {"JWT_AUTH_COOKIE": "jwt-auth-token"}
        mock_settings.SECRET_KEY = "secret_key"

        mock_cookie = MagicMock()
        mock_cookie.get.return_value = MagicMock(value='invalid_token')
        mock_SimpleCookie.return_value = mock_cookie

        mock_token_backend_instance = mock_TokenBackend.return_value
        mock_token_backend_instance.decode.side_effect = Exception("Invalid token")

        result = await game_io._check_authentication(environ, sid)

        assert result is False

@pytest.mark.asyncio
async def test_check_authentication_user_not_found():
    game_io = GameIO('/api/game')
    environ = {"HTTP_COOKIE": "jwt-auth-token=valid_token;"}
    sid = "test_sid"

    with patch("backend.GameIO.settings") as mock_settings, \
         patch("backend.GameIO.SimpleCookie") as mock_SimpleCookie, \
         patch("backend.GameIO.TokenBackend") as mock_TokenBackend, \
         patch("backend.GameIO.User.objects.aget", new=AsyncMock()) as mock_aget:
        
        mock_settings.REST_AUTH = {"JWT_AUTH_COOKIE": "jwt-auth-token"}
        mock_settings.SECRET_KEY = "secret_key"

        mock_cookie = MagicMock()
        mock_cookie.get.return_value = MagicMock(value='valid_token')
        mock_SimpleCookie.return_value = mock_cookie

        mock_token_backend_instance = mock_TokenBackend.return_value
        mock_token_backend_instance.decode.return_value = {"user_id": 1}

        mock_aget.side_effect = Exception("User not found")

        result = await game_io._check_authentication(environ, sid)

        assert result is False