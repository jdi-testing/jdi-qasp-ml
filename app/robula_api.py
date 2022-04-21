import json
import logging
import typing
from functools import wraps

from fastapi import APIRouter, Query, Request, status, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from redis.client import Redis
from starlette.responses import JSONResponse

from app.models import ReportModel, TaskIdModel, TaskResultModel, TaskStatusModel, XPathGenerationModel
from app.tasks import task_xpath_generation
from utils import api_utils
from utils.api_utils import send_report_email

logger = logging.getLogger("jdi-qasp-ml")
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exception_text = str(e)
            logger.exception(f"Error: {exception_text}")
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_text
            )

    return wrapper


@router.post("/schedule_xpath_generation", response_model=TaskIdModel)
@exception_handler
def schedule_xpath_generation(data: XPathGenerationModel):
    """Creates new celery task for xpath generation. Returns celery task id"""
    page = json.loads(data.document)

    task_result = task_xpath_generation.delay(
        api_utils.get_xpath_from_id(data.id), page, data.config.dict()
    )

    result = TaskIdModel(id=task_result.id)
    return JSONResponse(result.dict(), status.HTTP_201_CREATED)


@router.get("/get_task_status", response_model=TaskStatusModel)
@exception_handler
def get_task_status(id: str):
    """Returns status of generation task with specified id"""
    return api_utils.get_task_status(id)


@router.get("/get_tasks_statuses", response_model=typing.List[TaskStatusModel])
@exception_handler
def get_tasks_statuses(id: typing.List[str] = Query(None)):
    """Returns status of generation for tasks with specified ids"""
    results = api_utils.get_celery_task_statuses(id)
    return results


@router.post("/revoke_tasks")
@exception_handler
def revoke_task(task: TaskIdModel):
    """Revokes celery task with specified id"""
    api_utils.revoke_tasks(task.id)
    return JSONResponse({"result": "Tasks successfully revoked."})


@router.get("/get_task_result", response_model=TaskResultModel)
@exception_handler
def get_task_result(id: str):
    return JSONResponse(api_utils.get_task_result(id))


@router.get("/get_tasks_results", response_model=typing.List[TaskResultModel])
@exception_handler
def get_tasks_results(id: typing.List[str] = Query(None)):
    results = api_utils.get_celery_tasks_results(id)
    return JSONResponse(results)


@router.get("/celery_tasks")
def celery_tasks(request: Request):
    """Shows list of active (running, scheduled or reserved) celery tasks"""
    tasks = api_utils.get_active_celery_tasks()
    return templates.TemplateResponse(
        "tasks.html", {"request": request, "tasks": tasks}
    )


@router.post("/revoke_all_tasks")
def revoke_all_tasks():
    """Revokes all active (running, scheduled or reserved) tasks"""
    tasks = api_utils.get_active_celery_tasks()
    task_ids = [task["id"] for task in tasks]
    api_utils.revoke_tasks(task_ids=task_ids)
    return {"status": "ok", "tasksRevoked": task_ids}


@router.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    ws.created_tasks = []
    while True:
        try:
            data = await ws.receive_json()
            action = data["action"]
            payload = data["payload"]

            result = await api_utils.process_incoming_ws_request(action, payload, ws)

            if result:
                await ws.send_json(result)
        except KeyError:
            await ws.send_json({"error": "Invalid message format."})
        except WebSocketDisconnect:
            logger.info("socket disconnected")
            for task_result in ws.created_tasks:
                logger.info(f"Task revoked: {task_result.id}")
                task_result.revoke(terminate=True, signal="SIGKILL")


@router.post("/report_problem")
def report_problem(report: ReportModel):
    """
    Send email to SupportJDI@epam.com
    Screenshot(base64 encoded image)
    """
    with Redis('redis') as redis:
        prediction = redis.get('latest_prediction')
        send_report_email(report.subject, report.body, report.email, report.screenshot, prediction)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
