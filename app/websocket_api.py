import celery.states
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState


from app.logger import logger
from utils import api_utils

router = APIRouter()

async def process_and_send_result(action, payload, ws, logging_info):
    result = await api_utils.process_incoming_ws_request(action, payload, ws, logging_info)
    if result:
        await ws.send_json(result)

@router.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    ws.created_tasks = []

    async def handle_pong(payload):
        await ws.send_json({"pong": payload})
        logger.info("ANSWER TO PING WEBSOCKET MESSAGE IS SENT")

    while ws.client_state != WebSocketState.DISCONNECTED:
        try:
            data = await ws.receive_json()
            action = data["action"]
            payload = data["payload"]
            logging_info = data.get("logging_info")

            if action == "ping":
                # Immediately handle pong response in its own task
                asyncio.create_task(handle_pong(payload))

            # Process the incoming WebSocket request
            asyncio.create_task(process_and_send_result(action, payload, ws, logging_info))
        except KeyError as e:
            logger.error(e)
            await ws.send_json({"error": "Invalid message format."})
        except WebSocketDisconnect:
            from utils.api_utils import (
                revoked_tasks,
                tasks_vault,
                tasks_with_changed_priority,
            )

            tasks_vault.clear()
            tasks_with_changed_priority.clear()
            revoked_tasks.clear()
            logger.info("socket disconnected")
            for task_result in ws.created_tasks:
                if task_result.state in celery.states.UNREADY_STATES:
                    logger.info(f"Task revoked: {task_result.id}")
                    task_result.revoke(terminate=True, signal="SIGKILL")
