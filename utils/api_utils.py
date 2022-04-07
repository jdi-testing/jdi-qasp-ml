import asyncio
import base64
import json
import os
import typing
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO
from smtplib import SMTP, SMTP_SSL

from redis.client import Redis
from starlette.websockets import WebSocket

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


async def wait_until_task_reach_status(
    ws: WebSocket, task_id: str, expected_status: CeleryStatuses
):
    while True:
        task = get_task_status(task_id)
        if (
            (task.status in (CeleryStatuses.REVOKED, CeleryStatuses.FAILURE))
            or task.status == CeleryStatuses.SUCCESS
            and expected_status != CeleryStatuses.SUCCESS
        ):
            response = get_websocket_response(
                WebSocketResponseActions.STATUS_CHANGED, task.dict()
            )
            await ws.send_json(response)
            break

        if task.status == expected_status.value:
            await ws.send_json(
                get_websocket_response(
                    WebSocketResponseActions.STATUS_CHANGED, task.dict()
                )
            )
            if expected_status == CeleryStatuses.SUCCESS:
                result = get_task_result(task_id)
                await ws.send_json(
                    get_websocket_response(
                        WebSocketResponseActions.RESULT_READY, result
                    )
                )
            break
        await asyncio.sleep(0.5)


def get_websocket_response(action: WebSocketResponseActions, payload: dict) -> dict:
    return {"action": action.value, "payload": payload}


def revoke_tasks(task_ids: typing.List[str]):
    for task_id in task_ids:
        celery_app.control.revoke(task_id, terminate=True, signal="SIGKILL")


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


async def process_incoming_ws_request(
    action: str, payload: dict, ws: WebSocket
) -> typing.Dict:
    result = {}
    if action == "schedule_xpath_generation":
        payload = XPathGenerationModel(**payload)

        task_result = task_schedule_xpath_generation.delay(
            get_xpath_from_id(payload.id),
            json.loads(payload.document),
            payload.config.dict(),
        )
        ws.created_tasks.append(task_result)

        await ws.send_json(
            get_websocket_response(
                WebSocketResponseActions.TASKS_SCHEDULED, {payload.id: task_result.id}
            )
        )
        for status in [CeleryStatuses.STARTED, CeleryStatuses.SUCCESS]:
            asyncio.create_task(
                wait_until_task_reach_status(ws, task_result.id, status)
            )
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


def prepare_email_image(screenshot_base64) -> MIMEBase:
    part = MIMEBase('image', 'jpeg')
    with BytesIO(bytes(screenshot_base64, 'ascii')) as input_image, BytesIO() as decoded:
        base64.decode(input_image, decoded)
        decoded.seek(0)
        part.set_payload(decoded.read())

    encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename="screenshot.jpeg"')
    return part


def send_report_email(subject, body, email, screenshot_base64, prediction):
    msg = MIMEMultipart()
    msg['From'] = os.getenv('SUPPORT_EMAIL')
    msg['Subject'] = subject
    msg.attach(MIMEText(body + f'\nSender {email}' if body else f'\nSender: {email}'))
    msg.attach(prepare_email_image(screenshot_base64))

    with SMTP_SSL('smtp.mail.ru') as mail:
        if prediction:
            generated_json = MIMEBase('application', "json")
            generated_json.set_payload(prediction)
            generated_json.add_header('Content-Disposition',
                            'attachment; filename="gen.json"')
            msg.attach(generated_json)

        mail.login(os.getenv('SUPPORT_EMAIL'), os.getenv('SUPPORT_PASSWORD'))
        mail.sendmail(os.getenv('SUPPORT_EMAIL'), os.getenv('SUPPORT_EMAIL_INBOX'), msg.as_string())
