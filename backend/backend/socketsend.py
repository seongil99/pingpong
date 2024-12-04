from ingame.serializers import gameStateSerializer
from .sio import sio

import logging

logger = logging.getLogger("django")

default_namespace = "/api/game"

# 보낼 데이터만 받는걸로 수정
# 수정전 data -> InMemoryGameState
# 수정후 data -> InMemoryGameState.game_state['game_id'].render_data


async def socket_send(data, type, room_name, op=None):
    serialized_data = gameStateSerializer(data).data
    if type in ["gameStart", "gameState", "score"]:
        # Send the game state with type
        if not op:
            await sio.emit(
                "data",
                {**(serialized_data), "type": type},
                namespace=default_namespace,
                room=room_name,
            )
        else:
            await sio.emit(
                "data",
                {**(serialized_data), "type": type},
                to=op,
                namespace=default_namespace,
            )

    elif type == "gameWait" and op:
        # Send the 'gameWait' type to a specific socket
        await sio.emit("data", {"type": type}, to=op, namespace=default_namespace)

    elif type == "secondPlayer":
        # Handle sending data to second player
        # if not datais_single_player:
        await sio.emit("data", {"type": type}, to=op, namespace=default_namespace)
        await socket_send(data, "gameStart", room_name)

    elif not op:
        # If no 'op' socket is provided, send to all connected clients
        await sio.emit(
            "data", {"type": type}, namespace=default_namespace, room=room_name
        )

    elif type == "gameEnd":
        # Send 'gameEnd' data with additional text (op)
        await sio.emit(
            "data",
            {"type": type, "txt": op},
            namespace=default_namespace,
            room=room_name,
        )

    elif type == "sound":
        # Send sound data
        await sio.emit(
            "data",
            {"type": type, "sound": op},
            namespace=default_namespace,
            room=room_name,
        )

    elif type == "effect":
        # Send effect data
        await sio.emit(
            "data",
            {"type": type, "op": op},
            namespace=default_namespace,
            room=room_name,
        )
