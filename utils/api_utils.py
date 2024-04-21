import asyncio
import json
import typing
import uuid
from pathlib import Path

from celery.result import AsyncResult
from starlette.websockets import WebSocket, WebSocketState
from websockets.exceptions import ConnectionClosedOK

import app.mongodb as mongodb
from app.celery_app import celery_app
from app.constants import CeleryStatuses, WebSocketResponseActions
from app.css_locators import inject_css_selector_generator_scripts, CSS_SELECTOR_GEN_TASK_PREFIX
from app.logger import logger
from app.models import LoggingInfoModel, TaskStatusModel, XPathGenerationModel, CSSSelectorGenerationModel
from app.redis_app import redis_app
from app.selenium_app import get_chunks_boundaries
from app.tasks import ENV, task_schedule_xpath_generation, task_schedule_css_selector_generation

from utils import config as app_config


def get_task_status(task_id) -> TaskStatusModel:
    result = TaskStatusModel(
        id=task_id, status=celery_app.AsyncResult(task_id).status
    )
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
    ws: WebSocket,
    task_result_obj: AsyncResult,
    expected_status: CeleryStatuses,
):
    while ws.client_state != WebSocketState.DISCONNECTED:
        task_id = task_result_obj.id
        task = get_task_status(task_id)
        if (
            task.status in (CeleryStatuses.REVOKED, CeleryStatuses.FAILURE)
        ) or (
            task.status == CeleryStatuses.SUCCESS
            and expected_status != CeleryStatuses.SUCCESS
        ):
            if task_id not in tasks_with_changed_priority:
                task_dict = task.model_dump()
                # deleting underscores in task_id if any to send to frontend
                task_dict["id"] = task_dict["id"].strip("_")

                # Informing frontend about failed elements from
                # task_schedule_css_locator_generation task, because otherwise
                # this info will be lost. In schedule_multiple_xpath_generations task
                # the id of an element is the task id, so it doesn't need this logic
                if task_id.startswith(CSS_SELECTOR_GEN_TASK_PREFIX):
                    task_dict["elements_ids"] = task_result_obj.kwargs.get("elements_ids")

                error_message = str(task_result_obj.result)
                response = get_websocket_response(
                    action=WebSocketResponseActions.STATUS_CHANGED,
                    payload=task_dict,
                    error_message=error_message,
                )
                try:
                    await ws.send_json(response)
                except (ConnectionClosedOK, RuntimeError):
                    break
                break

        if task.status == expected_status.value:
            task_dict = task.model_dump()
            # deleting underscores in task_id if any to send to frontend
            task_dict["id"] = task_dict["id"].strip("_")

            if expected_status == CeleryStatuses.SUCCESS:
                result = get_task_result(task_id)
                # deleting underscores in task_id if any to send to frontend
                result["id"] = result["id"].strip("_")

                if ENV != "LOCAL":
                    session_id = task_result_obj.kwargs.get("session_id")
                    website_url = task_result_obj.kwargs.get("website_url")
                    start_time = task_result_obj.kwargs.get("start_time")
                    task_duration = task_result_obj.kwargs.get("task_duration")
                    full_xpath = task_result_obj.kwargs.get("full_xpath")
                    nesting_num = task_result_obj.kwargs.get("nesting_num")
                    await mongodb.enrich_logs_with_generated_locators(
                        session_id,
                        website_url,
                        full_xpath,
                        nesting_num,
                        result,
                        start_time,
                        task_duration,
                    )
                try:
                    await ws.send_json(
                        get_websocket_response(
                            WebSocketResponseActions.RESULT_READY, result
                        )
                    )
                except (ConnectionClosedOK, RuntimeError):
                    break
            break
        await asyncio.sleep(0.5)


def get_websocket_response(
    action: WebSocketResponseActions, payload: dict, error_message=None
) -> dict:
    message_to_return = {"action": action.value, "payload": payload}
    if error_message is not None:
        message_to_return["error_message"] = error_message
    return message_to_return


def task_is_revoked(task_id: str):
    task_instance = celery_app.AsyncResult(task_id)
    task_status = task_instance.status
    return task_status == "REVOKED"


def task_exists(task_id: str):
    task_instance = celery_app.AsyncResult(task_id)
    task_status = task_instance.status
    return task_status != "PENDING"


def task_exists_and_already_succeeded(task_id: str):
    task_instance = celery_app.AsyncResult(task_id)
    task_status = task_instance.status
    return task_status == "SUCCESS"


def task_started_and_running(task_id: str):
    task_instance = celery_app.AsyncResult(task_id)
    task_status = task_instance.status
    return task_status == "STARTED"


def convert_task_id_if_exists(task_id: str):
    if task_exists(task_id):
        return convert_task_id_if_exists(f"_{task_id}")

    return task_id


def convert_task_id_if_not_running(task_id: str):
    if not task_started_and_running(task_id):
        return convert_task_id_if_not_running(f"_{task_id}")

    return task_id


def convert_task_id_if_in_revoked(task_id: str):
    task_instance = celery_app.AsyncResult(task_id)
    task_status = task_instance.status
    logger.info(
        "Command to revoke task - %s with status %s", task_id, task_status
    )
    if task_status == "REVOKED":
        logger.info("Task is already revoked. task_id -> _task_id")
        return f"_{task_id}"
    return task_id


revoked_tasks = set()


def revoke_tasks(task_ids: typing.List[str]):
    for task_id in task_ids:
        task_id = convert_task_id_if_in_revoked(task_id)
        celery_app.control.revoke(task_id, terminate=True)
        revoked_tasks.add(task_id)


def get_celery_tasks_results(ids: typing.List) -> typing.List[dict]:
    results = []
    for task_id in ids:
        results.append(get_task_result(task_id))
    return results


def get_celery_task_statuses(ids: typing.List[str]):
    results = []
    for task_id in ids:
        results.append(get_task_status(task_id).model_dump())
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


tasks_vault = {}
tasks_with_changed_priority = set()


async def change_task_priority(ws, payload, priority):
    id_of_task_to_change_priority = payload["element_id"]
    tasks_with_changed_priority.add(id_of_task_to_change_priority)
    revoke_tasks([id_of_task_to_change_priority])

    task_kwargs = tasks_vault[id_of_task_to_change_priority]
    id_of_task_to_change_priority = convert_task_id_if_in_revoked(
        id_of_task_to_change_priority
    )
    new_task_result = task_schedule_xpath_generation.apply_async(
        kwargs=task_kwargs,
        task_id=id_of_task_to_change_priority,
        zpriority=priority,
    )
    ws.created_tasks.append(new_task_result)

    asyncio.create_task(
        wait_until_task_reach_status(
            ws=ws,
            task_result_obj=new_task_result,
            expected_status=CeleryStatuses.SUCCESS,
        )
    )


async def process_incoming_ws_request(
    action: str, payload: dict, ws: WebSocket, logging_info: dict
) -> typing.Dict:
    result = {}

    if action == "ping":
        await ws.send_json({"pong": payload})
        logger.info("ANSWER TO PING WEBSOCKET MESSAGE FOR IS SENT")

    elif action == "schedule_multiple_xpath_generations":
        logging_info = LoggingInfoModel(**logging_info)
        if ENV != "LOCAL":
            mongodb.create_initial_log_entry(
                logging_info
            )  # for custom metrics logging purposes

        payload = XPathGenerationModel(**payload)
        element_ids = payload.id
        document = json.loads(payload.document)

        random_document_key = str(uuid.uuid4())
        # saving document (website content) to redis -
        # we cache it because we'll reuse it n times, where 'n' - number of elements
        redis_app.set(name=random_document_key, value=document)

        config = payload.config.model_dump()

        for element_id in element_ids:
            if task_exists_and_already_succeeded(
                element_id
            ) and not config.get("advanced_calculation"):
                logger.info("Using cached result for task_id %s", element_id)
                task_result_obj = AsyncResult(element_id)
                asyncio.create_task(
                    wait_until_task_reach_status(
                        ws=ws,
                        task_result_obj=task_result_obj,
                        expected_status=CeleryStatuses.SUCCESS,
                    )
                )
            else:
                new_task_id = convert_task_id_if_exists(element_id)
                task_kwargs = {
                    "session_id": logging_info.session_id,  # for custom metrics logging purposes
                    "website_url": logging_info.website_url,  # for custom metrics logging purposes
                    "element_id": get_xpath_from_id(element_id),
                    "document_uuid": random_document_key,
                    "config": config,
                }
                tasks_vault[element_id] = task_kwargs

                task_result_obj = task_schedule_xpath_generation.apply_async(
                    kwargs=task_kwargs, task_id=new_task_id, zpriority=2
                )
                ws.created_tasks.append(task_result_obj)

                asyncio.create_task(
                    wait_until_task_reach_status(
                        ws=ws,
                        task_result_obj=task_result_obj,
                        expected_status=CeleryStatuses.SUCCESS,
                    )
                )
    elif action == "prioritize_existing_task":
        await change_task_priority(ws, payload, priority=1)

    elif action == "deprioritize_existing_task":
        await change_task_priority(ws, payload, priority=3)

    elif action == "get_task_status":
        result = get_task_status(payload["id"]).model_dump()
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
        result = get_celery_tasks_results(payload["id"])
    elif action == "schedule_css_locators_generation":
        generation_data = CSSSelectorGenerationModel(**payload)
        elements_ids = generation_data.id

        document = generation_data.document
        random_document_key = str(uuid.uuid4())
        html_file = Path(f"analyzed_pages/{random_document_key}.html")
        html_file.write_text(inject_css_selector_generator_scripts(document))
        selectors_generation_results = []

        num_of_tasks = app_config.SELENOID_PARALLEL_SESSIONS_COUNT
        jobs_chunks = get_chunks_boundaries(elements_ids, num_of_tasks)

        for start_idx, end_idx in jobs_chunks:
            task_id = convert_task_id_if_exists(
                f"{CSS_SELECTOR_GEN_TASK_PREFIX}{uuid.uuid4()}"
            )
            task_kwargs = {
                "document_path": str(html_file),
                "elements_ids": elements_ids[start_idx:end_idx]
            }

            task_result_obj = task_schedule_css_selector_generation.apply_async(
                kwargs=task_kwargs, task_id=task_id, zpriority=2
            )
            selectors_generation_results.append(task_result_obj)
            ws.created_tasks.append(task_result_obj)

        celery_waiting_tasks = set()
        for result_obj in selectors_generation_results:
            celery_waiting_tasks.add(
                asyncio.create_task(
                    wait_until_task_reach_status(
                        ws=ws,
                        task_result_obj=result_obj,
                        expected_status=CeleryStatuses.SUCCESS,
                    )
                )
            )
        await asyncio.wait(celery_waiting_tasks)
        html_file.unlink()

    return result


def sort_predict_body(request_body):
    body_as_python_obj = json.loads(request_body.decode("utf-8"))
    body_as_python_obj_sorted = list(
        sorted(body_as_python_obj, key=lambda x: int(x["element_id"]))
    )
    body_sorted = json.dumps(
        body_as_python_obj_sorted, ensure_ascii=False
    ).encode("utf-8")
    return body_sorted
