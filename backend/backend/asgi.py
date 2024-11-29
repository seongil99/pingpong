"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .socketsend import socket_send

# from .socketsend import socket_send
import socketio

import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
logger = logging.getLogger("django")


sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    namespaces=["/api/game"],
)

from ingame.game_logic import PingPongServer

game = PingPongServer(sio)


class GameIO(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        sio.emit("data", {"response": "my response"}, namespace="/api/game")
        logger.info(f"Client connected: {sid}")
        data = game.game_state
        data.clients[sid] = sid  # Replace with your actual client storage logic

        if len(data.clients) > 1:
            await socket_send(data, sio, "secondPlayer", sid)
            await socket_send(data, sio, "gameStart")
            data.gameStart = True
            game.game_loop()
        else:
            logger.info("Waiting for another player...")
            logger.info(f"is single player: {data.is_single_player}")
            await socket_send(data, sio, "gameWait", sid)
            if data.is_single_player:
                await socket_send(data, sio, "gameStart")
                data.gameStart = True
                game.game_loop()

        await socket_send(data, sio, "gameState", sid)

    async def on_keyPress(self, sid, data):
        logger.info(f"Key press: {data}")
        if data["key"] != " ":
            game.handle_player_input(sid, data["key"], data["pressed"])
        else:
            player = (
                game.my_game_state["playerOne"]
                if not data.get("who")
                else game.my_game_state["playerTwo"]
            )
            is_collision = [
                ball
                for ball in game.my_game_state["balls"]
                if game.is_in_range(int(ball.position["x"]), int(player["x"]), 10)
                and game.is_in_range(int(ball.position["z"]), int(player["z"]), 10)
            ]
            if len(is_collision) == 1:
                game.set_ball_velocity(is_collision[0], 2)
                logger.info(f"Collision: {is_collision[0].position}")
                await socket_send(
                    game.game_state, sio, "effect", is_collision[0].position
                )

    async def on_disconnect(self, sid):
        logger.info(f"Client disconnected: {sid}")
        if sid in game.game_state.clients:
            del game.game_state.clients[sid]


sio.register_namespace(GameIO("/api/game"))


django_asgi_app = get_asgi_application()

game_app = socketio.ASGIApp(sio, socketio_path="/api/game/socket.io")

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Handle HTTP traffic
        "websocket": AuthMiddlewareStack(game_app),
        # "websocket": URLRouter(
        #     [  # WebSocket routing
        #         path("api/game/", game_app),
        #         path("api/game/socket.io/", game_app),
        #     ]
        # ),
    }
)

import asyncio
from django.core.signals import request_finished
from django.dispatch import receiver


# @receiver(request_finished)
# async def loop(sender, **kwargs):
#     try:
#         asyncio.create_task(game.game_loop())
#     except Exception as e:
#         logger.error(e)


# asyncio.run(main())
