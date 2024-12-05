from ingame.game_logic import PingPongServer
from backend.sio import sio
from backend.socketsend import socket_send
from ingame.data import user_to_game
from urllib.parse import parse_qs

import socketio
import logging
import uuid

logger = logging.getLogger("django")

server = PingPongServer(sio)
game_state_db = server.game_state


# mock_game_id = str(uuid.uuid4())  # Example: 'e4d909c2-6b18-11ed-81ce-0242ac120002'


class GameIO(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ, auth):
        logger.info(f"Client connected: {sid}")
        query = environ.get('QUERY_STRING', '')
        params = parse_qs(query)
        game_id = "room_" + params.get("gameId", [""])[0]
        user_name = params.get("userName", [""])[0]
        # enter game room
        await sio.enter_room(sid, game_id, namespace="/api/game")
        logger.info(f"rooms: {sio.manager.rooms}")
        # save user sid to game_id
        user_to_game[sid] = game_id
        server.add_game(sid, game_id, user_name)  # 유저이름 변경 필요 받아야 할듯
        game_state = game_state_db.load_game_state(game_id)
        # game_state["is_single_player"] = True
        logger.info(f"game_state: {game_state}")
        if len(game_state["clients"]) > 1:
            logger.info("Two players are ready!")
            await socket_send(game_state["render_data"], "secondPlayer", game_id, sid)
            await socket_send(game_state["render_data"], "gameStart", game_id)
            game_state["gameStart"] = True
            server.game_loop(game_state)
        else:
            logger.info("Waiting for another player...")
            logger.info(f"is single player: {game_state['is_single_player']}")
            await socket_send(game_state["render_data"], "gameWait", game_id, sid)
            if game_state["is_single_player"]:
                await socket_send(game_state["render_data"], "gameStart", game_id)
                logger.info("Single player game start")
                game_state["gameStart"] = True
                server.game_loop(game_state)

        await socket_send(game_state["render_data"], "gameState", sid, game_id)

    async def on_keyPress(self, sid, data):
        logger.info(f"Key press: {data}")
        game_id = user_to_game[sid]
        game_state = server.game_state.load_game_state(game_id)
        if data["key"] != " ":
            server.handle_player_input(game_state, sid, data["key"], data["pressed"])
        else:
            player = (
                game_state["render_data"]["playerOne"]
                if not data.get("who")
                else game_state["render_data"]["playerTwo"]
            )
            is_collision = [
                ball
                for ball in game_state["render_data"]["balls"]
                if server.is_in_range(int(ball.position["x"]), int(player["x"]), 10)
                   and server.is_in_range(int(ball.position["z"]), int(player["z"]), 10)
            ]
            if len(is_collision) == 1:
                server.set_ball_velocity(game_state, is_collision[0], 2)
                logger.info(f"Collision: {is_collision[0].position}")
                await socket_send(
                    game_state["render_data"],
                    "effect",
                    game_id,
                    is_collision[0].position,
                )

    async def on_disconnect(self, sid):
        logger.info(f"Client disconnected: {sid}")
        game_id = user_to_game[sid]
        game_state = server.game_state.load_game_state(game_id)
        if sid in game_state["clients"]:
            del game_state["clients"][sid]
        if len(game_state["clients"]) == 0:
            game_state_db.delete_game_state(game_id)
