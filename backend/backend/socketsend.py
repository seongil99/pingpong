import logging
from ingame.serializers import gameStateSerializer
from .sio import sio


logger = logging.getLogger("django")

DEFAULT_NAMESPACE = "/api/game"

# 보낼 데이터만 받는걸로 수정
# 수정전 data -> InMemoryGameState
# 수정후 data -> InMemoryGameState.game_state['game_id'].render_data


async def socket_send(data, data_type, room_name, op=None):
    """
    소켓전송을 도와주는 함수
    """
    serialized_data = gameStateSerializer(data).data
    if data_type in ["gameStart", "gameState", "score"]:
        # Send the game state with type
        if not op:
            await sio.emit(
                "data",
                {**(serialized_data), "type": data_type},
                namespace=DEFAULT_NAMESPACE,
                room=room_name,
            )
        else:
            await sio.emit(
                "data",
                {**(serialized_data), "type": data_type},
                to=op,
                namespace=DEFAULT_NAMESPACE,
            )

    elif data_type == "gameWait" and op:
        # Send the 'gameWait' type to a specific socket
        await sio.emit("data", {"type": data_type}, to=op, namespace=DEFAULT_NAMESPACE)

    elif data_type == "secondPlayer":
        # Handle sending data to second player
        # if not datais_single_player:
        await sio.emit("data", {"type": data_type}, to=op, namespace=DEFAULT_NAMESPACE)
        await socket_send(data, "gameStart", room_name)

    elif not op:
        # If no 'op' socket is provided, send to all connected clients
        await sio.emit(
            "data", {"type": data_type}, namespace=DEFAULT_NAMESPACE, room=room_name
        )

    elif data_type == "gameEnd":
        # Send 'gameEnd' data with additional text (op)
        await sio.emit(
            "data",
            {"type": data_type, "txt": op},
            namespace=DEFAULT_NAMESPACE,
            room=room_name,
        )

    elif data_type == "sound":
        # Send sound data
        await sio.emit(
            "data",
            {"type": data_type, "sound": op},
            namespace=DEFAULT_NAMESPACE,
            room=room_name,
        )

    elif data_type == "effect":
        # Send effect data
        await sio.emit(
            "data",
            {"type": data_type, "op": op},
            namespace=DEFAULT_NAMESPACE,
            room=room_name,
        )
