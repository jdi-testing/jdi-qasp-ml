import asyncio
import json
import logging

from fastapi import APIRouter
from fastapi.websockets import WebSocket

from app.constants import CeleryStatuses, WebSocketResponseActions
from app.models import XPathGenerationModel
from app.tasks import task_schedule_xpath_generation
from utils import api_utils

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
            result = {}
            if action == "schedule_xpath_generation":
                payload = XPathGenerationModel(**payload)

                task_result = task_schedule_xpath_generation.delay(
                    api_utils.get_xpath_from_id(payload.id),
                    json.loads(payload.document),
                    payload.config.dict()
                )
                await ws.send_json(api_utils.get_websocket_response(WebSocketResponseActions.TASKS_SCHEDULED,
                                                                    {payload.id: task_result.id}))
                for status in [CeleryStatuses.STARTED, CeleryStatuses.SUCCESS]:
                    asyncio.create_task(api_utils.wait_until_task_reach_status(ws, task_result.id, status))
            elif action == "get_task_status":
                result = api_utils.get_task_status(payload["id"]).dict()
            elif action == "get_tasks_statuses":
                task_ids = payload["id"]
                result = api_utils.get_celery_task_statuses(task_ids)
            elif action == "revoke_tasks":
                api_utils.revoke_tasks(payload["id"])
                result = {"result": "Tasks successfully revoked."}
            elif action == "get_task_result":
                result = api_utils.get_task_result(payload["id"])
            elif action == "get_task_results":
                result = api_utils.get_celery_tasks_results(payload)
            if result:
                await ws.send_json(result)
        except KeyError:
            await ws.send_json({"error": "Invalid message format."})
