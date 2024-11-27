from .game_logic import PingPongServer

import logging

logger = logging.getLogger("django")
game = PingPongServer()


@sio.event
async def connect(sid, environ):
    logger.info(f"New client connected: {sid}")
    game.clients[sid] = sid  # Replace with your actual client storage logic

    if len(game.clients) > 1:
        await game.socket_send("secondPlayer", sid)
        await game.socket_send("gameStart")
        game.gameStart = True
    else:
        print("Waiting for another player...")
        await game.socket_send("gameWait", sid)
        if game.isSinglePlayer:
            await game.socket_send("gameStart")
            game.gameStart = True

    await game.socket_send("gameState", sid)


@sio.event
async def keyPress(sid, data):
    if data["key"] != " ":
        game.handle_player_input(sid, data["key"], data["pressed"])
    else:
        player = (
            game.gameState.playerOne
            if not data.get("who")
            else game.gameState.playerTwo
        )
        is_collision = [
            ball
            for ball in game.gameState.balls
            if game.is_in_range(int(ball.position.x), int(player.x), 10)
            and game.is_in_range(int(ball.position.z), int(player.z), 10)
        ]
        if len(is_collision) == 1:
            game.set_ball_velocity(is_collision[0], 2)
            await game.socket_send("effect", is_collision[0].position)


@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    if sid in game.clients:
        del game.clients[sid]
