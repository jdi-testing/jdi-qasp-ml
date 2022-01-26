import logging

from fastapi import APIRouter
from fastapi.websockets import WebSocket

from utils.api_utils import process_incoming_ws_request

router = APIRouter()
logger = logging.getLogger("jdi-qasp-ml")


@router.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_json()
        try:
            action = data["action"]
            payload = data["payload"]

            result = await process_incoming_ws_request(action, payload, ws)

            if result:
                await ws.send_json(result)
        except KeyError:
            await ws.send_json({"error": "Invalid message format."})
