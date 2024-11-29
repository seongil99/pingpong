from .game_logic import PingPongServer

import logging
import socketio

logger = logging.getLogger(__name__)
game = PingPongServer()

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    namespaces=["/api/game"],
)

class GameIO(socketio.AsyncNamespace):

    async def on_connect(self, sid, environ, auth):
        sio.emit("data", {"response": "my response"})
        game_state = game.game_state
        game_state.clients[sid] = sid  # Replace with your actual client storage logic

        if len(game_state.clients) > 1:
            await socket_send("secondPlayer", sid)
            await socket_send("gameStart")
            game_state.gameStart = True
        else:
            print("Waiting for another player...")
            await socket_send("gameWait", sid)
            if game_state.is_single_player:
                await socket_send("gameStart")
                game_state.gameStart = True

        await socket_send("gameState", sid)

    async def on_keyPress(self, sid, data):
        logger.info(f"Key press: {data}")
        if data["key"] != " ":
            game.handle_player_input(sid, data["key"], data["pressed"])
        else:
            player = (
                game.game_state.playerOne
                if not data.get("who")
                else game.game_state.playerTwo
            )
            is_collision = [
                ball
                for ball in game.game_state.balls
                if game.is_in_range(int(ball.position.x), int(player.x), 10)
                and game.is_in_range(int(ball.position.z), int(player.z), 10)
            ]
            if len(is_collision) == 1:
                game.set_ball_velocity(is_collision[0], 2)
                await socket_send("effect", is_collision[0].position)

    async def on_disconnect(self, sid):
        logger.info(f"Client disconnected: {sid}")
        if sid in game.game_state.clients:
            del game.game_state.clients[sid]


async def socket_send(type, op=None):
    if type in ["gameStart", "gameState", "score"]:
        # Send the game state with type
        if not op:
            await sio.emit("data", {**game.game_state, "type": type})
        else:
            await op.emit("data", {**game.game_state, "type": type})

    elif type == "gameWait" and op:
        # Send the 'gameWait' type to a specific socket
        await op.emit("data", {"type": type})

    elif type == "secondPlayer":
        # Handle sending data to second player
        if not game.game_state.is_single_player:
            await sio.emit("data", {"type": type}, room=op)
        await socket_send("gameStart")

    elif not op:
        # If no 'op' socket is provided, send to all connected clients
        await sio.emit("data", {"type": type})

    elif type == "gameEnd":
        # Send 'gameEnd' data with additional text (op)
        await sio.emit("data", {"type": type, "txt": op})

    elif type == "sound":
        # Send sound data
        await sio.emit("data", {"type": type, "sound": op})

    elif type == "effect":
        # Send effect data
        await sio.emit("data", {"type": type, "effect": op})
