from ingame.serializers import InMemoryGameStateSerializer

import logging

logger = logging.getLogger("django")

default_namespace = "/api/game"


async def socket_send(data, sio, type, op=None):
    # logger.info(f"data: {data.game_state}")
    serialized_data = InMemoryGameStateSerializer(data).data
    # logger.info(f"serialized_data: {serialized_data}")
    if type in ["gameStart", "gameState", "score"]:
        # Send the game state with type
        if not op:
            await sio.emit(
                "data",
                {**(serialized_data["game_state"]), "type": type},
                namespace=default_namespace,
            )
        else:
            await sio.emit(
                "data",
                {**(serialized_data["game_state"]), "type": type},
                to=op,
                namespace=default_namespace,
            )

    elif type == "gameWait" and op:
        # Send the 'gameWait' type to a specific socket
        await sio.emit("data", {"type": type}, to=op, namespace=default_namespace)

    elif type == "secondPlayer":
        # Handle sending data to second player
        if not data.game_state.is_single_player:
            await sio.emit("data", {"type": type}, room=op, namespace=default_namespace)
        await socket_send("gameStart")

    elif not op:
        # If no 'op' socket is provided, send to all connected clients
        await sio.emit("data", {"type": type}, namespace=default_namespace)

    elif type == "gameEnd":
        # Send 'gameEnd' data with additional text (op)
        await sio.emit("data", {"type": type, "txt": op}, namespace=default_namespace)

    elif type == "sound":
        # Send sound data
        await sio.emit("data", {"type": type, "sound": op}, namespace=default_namespace)

    elif type == "effect":
        # Send effect data
        await sio.emit(
            "data", {"type": type, "effect": op}, namespace=default_namespace
        )
