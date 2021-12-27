import json
import logging
import typing
from functools import wraps

from fastapi import APIRouter
from fastapi import status
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.celery_app import celery_app
from app.models import XPathGenerationModel, TaskIdModel
from app.tasks import task_schedule_xpath_generation
from utils import api_utils
from utils.api_utils import get_xpath_from_id

logger = logging.getLogger("jdi-qasp-ml")
router = APIRouter()


def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            exception_text = str(e)
            logger.exception(f'Error: {exception_text}')
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=exception_text)

    return wrapper


@router.post('/schedule_xpath_generation')
@exception_handler
def schedule_xpath_generation(data: XPathGenerationModel):
    """ Creates new celery task for xpath generation. Returns celery task id """
    page = json.loads(data.document)

    task_result = task_schedule_xpath_generation.delay(get_xpath_from_id(data.id), page, data.config.dict())
    result = {'task_id': task_result.id}
    return JSONResponse(result, status.HTTP_201_CREATED)


@router.get('/get_task_status')
@exception_handler
def get_task_status(id: str):
    """ Returns status of generation task with specified id """
    return JSONResponse(api_utils.get_task_status(id))


@router.get('/get_tasks_statuses')
@exception_handler
def get_tasks_statuses(ids: typing.List[str]):
    """ Returns status of generation for tasks with specified ids """
    results = []
    for id in ids:
        results.append(api_utils.get_task_status(id))
    return JSONResponse(results)


@router.post('/revoke_task')
@exception_handler
def revoke_task(task: TaskIdModel):
    """ Revokes celery task with specified id """
    celery_app.control.revoke(task.id, terminate=True, signal='SIGKILL')
    return JSONResponse({'result': 'Task successfully revoked.'})


@router.get('/get_task_result')
@exception_handler
def get_task_result(id: str):
    return JSONResponse(api_utils.get_task_result(id))


@router.get('/get_tasks_results')
@exception_handler
def get_tasks_results(task_ids: typing.List[str]):
    results = []
    for task_id in task_ids:
        results.append(api_utils.get_task_result(task_id))
    return JSONResponse(results)
