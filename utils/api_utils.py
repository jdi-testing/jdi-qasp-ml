import asyncio
import json
import typing

from starlette.websockets import WebSocket, WebSocketState

from app.celery_app import celery_app
from app.constants import CeleryStatuses, WebSocketResponseActions
from app.models import TaskStatusModel, XPathGenerationModel
from app.tasks import task_schedule_xpath_generation


def get_task_status(task_id) -> TaskStatusModel:
    result = TaskStatusModel(id=task_id, status=celery_app.AsyncResult(task_id).status)
    return result


def get_task_result(task_id):
    result = celery_app.AsyncResult(task_id)
    if result.status == "SUCCESS":
        return {"id": task_id, "result": result.get()}
    else:
        return {"id": task_id, "exc": "Generation still in progress."}


def get_xpath_from_id(element_id):
    """
    Returns xpath based on jdn_hash
    :param element_id:
    :return: xpath
    """
    return f"//*[@jdn-hash='{element_id}']"


def get_element_id_from_xpath(xpath: str):
    """
    "//*[@jdn-hash='{element_id}']" -> "{element_id}"
    """
    return xpath.split("'")[1]


async def wait_until_task_reach_status(
    ws: WebSocket, task_id: str, expected_status: CeleryStatuses
):
    while ws.client_state != WebSocketState.DISCONNECTED:
        task = get_task_status(task_id)
        if (
            (task.status in (CeleryStatuses.REVOKED, CeleryStatuses.FAILURE))
            or task.status == CeleryStatuses.SUCCESS
            and expected_status != CeleryStatuses.SUCCESS
        ):
            task_dict = task.dict()
            # deleting underscores in task_id if any to send to frontend
            task_dict["id"] = task_dict["id"].strip("_")
            response = get_websocket_response(
                WebSocketResponseActions.STATUS_CHANGED, task_dict
            )
            await ws.send_json(response)
            break

        if task.status == expected_status.value:
            task_dict = task.dict()
            # deleting underscores in task_id if any to send to frontend
            task_dict["id"] = task_dict["id"].strip("_")
            await ws.send_json(
                get_websocket_response(
                    WebSocketResponseActions.STATUS_CHANGED, task_dict
                )
            )
            if expected_status == CeleryStatuses.SUCCESS:
                result = get_task_result(task_id)
                # deleting underscores in task_id if any to send to frontend
                result["id"] = result["id"].strip("_")
                await ws.send_json(
                    get_websocket_response(
                        WebSocketResponseActions.RESULT_READY, result
                    )
                )
            break
        await asyncio.sleep(0.5)


def get_websocket_response(action: WebSocketResponseActions, payload: dict) -> dict:
    return {"action": action.value, "payload": payload}


def convert_task_id_if_in_revoked(task_id: str):
    if task_id in revoked_tasks_ids_set:
        return convert_task_id_if_in_revoked(f"_{task_id}")

    return task_id


def revoke_tasks(task_ids: typing.List[str]):
    for task_id in task_ids:
        task_id = convert_task_id_if_in_revoked(task_id)
        celery_app.control.revoke(task_id, terminate=True)
        revoked_tasks_ids_set.add(task_id)


def get_celery_tasks_results(ids: typing.List) -> typing.List[dict]:
    results = []
    for task_id in ids:
        results.append(get_task_result(task_id))
    return results


def get_celery_task_statuses(ids: typing.List[str]):
    results = []
    for task_id in ids:
        results.append(get_task_status(task_id))
    return results


def get_active_celery_tasks():
    celery_tasks = []
    inspect = celery_app.control.inspect()
    active = inspect.active().values()
    scheduled = inspect.scheduled().values()
    reserved = inspect.reserved().values()

    for task_list in [active, scheduled, reserved]:
        for tasks in task_list:
            celery_tasks.extend(tasks)

    return celery_tasks


revoked_tasks_ids_set = set()
tasks_vault = {}


async def change_task_priority(ws, payload, priority):
    id_of_task_to_change_priority = payload["element_id"]
    revoke_tasks([id_of_task_to_change_priority])

    task_kwargs = tasks_vault[id_of_task_to_change_priority]
    id_of_task_to_change_priority = convert_task_id_if_in_revoked(
        id_of_task_to_change_priority
    )
    new_task_result = task_schedule_xpath_generation.apply_async(
        kwargs=task_kwargs, task_id=id_of_task_to_change_priority, zpriority=priority
    )
    ws.created_tasks.append(new_task_result)

    task_id_to_show = id_of_task_to_change_priority.strip("_")
    new_task_result_id_to_show = new_task_result.id.strip("_")
    await ws.send_json(
        get_websocket_response(
            WebSocketResponseActions.TASKS_SCHEDULED,
            {task_id_to_show: new_task_result_id_to_show},
        )
    )
    for status in [CeleryStatuses.STARTED, CeleryStatuses.SUCCESS]:
        asyncio.create_task(
            wait_until_task_reach_status(ws, new_task_result.id, status)
        )


async def process_incoming_ws_request(
    action: str, payload: dict, ws: WebSocket
) -> typing.Dict:
    result = {}

    if action == "schedule_multiple_xpath_generations":
        payload = XPathGenerationModel(**payload)
        element_ids = payload.id
        for element_id in element_ids:
            new_task_id = convert_task_id_if_in_revoked(element_id)
            task_kwargs = {
                "element_id": get_xpath_from_id(element_id),
                "document": json.loads(payload.document),
                "config": payload.config.dict(),
            }
            tasks_vault[element_id] = task_kwargs
            task_result = task_schedule_xpath_generation.apply_async(
                kwargs=task_kwargs, task_id=new_task_id, zpriority=2
            )
            ws.created_tasks.append(task_result)

            element_id_to_show = element_id.strip("_")
            task_result_id_to_show = task_result.id.strip("_")
            await ws.send_json(
                get_websocket_response(
                    WebSocketResponseActions.TASKS_SCHEDULED,
                    {element_id_to_show: task_result_id_to_show},
                )
            )
            for status in [CeleryStatuses.STARTED, CeleryStatuses.SUCCESS]:
                asyncio.create_task(
                    wait_until_task_reach_status(ws, task_result.id, status)
                )
    elif action == "prioritize_existing_task":
        await change_task_priority(ws, payload, priority=1)

    elif action == "deprioritize_existing_task":
        pass

    elif action == "get_task_status":
        result = get_task_status(payload["id"]).dict()
    elif action == "get_tasks_statuses":
        task_ids = payload["id"]
        result = get_celery_task_statuses(task_ids)
    elif action == "revoke_tasks":
        revoke_tasks(payload["id"])
        result = get_websocket_response(
            WebSocketResponseActions.TASKS_REVOKED, {"id": payload["id"]}
        )
    elif action == "get_task_result":
        result = get_task_result(payload["id"])
    elif action == "get_task_results":
        result = get_celery_tasks_results(payload)

    return result
