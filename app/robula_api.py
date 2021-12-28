import json
import logging
import typing
from functools import wraps

from fastapi import APIRouter, Query
from fastapi import status
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse

from app.models import XPathGenerationModel, TaskIdModel, TaskStatusModel, TaskIdsModel, TaskResultModel
from app.tasks import task_schedule_xpath_generation
from utils import api_utils
from utils.api_utils import get_celery_task_statuses

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


@router.post('/schedule_xpath_generation', response_model=TaskIdModel)
@exception_handler
def schedule_xpath_generation(data: XPathGenerationModel):
    """ Creates new celery task for xpath generation. Returns celery task id """
    page = json.loads(data.document)

    task_result = task_schedule_xpath_generation.delay(api_utils.get_xpath_from_id(data.id), page, data.config.dict())

    result = TaskIdModel(id=task_result.id)
    return JSONResponse(result.dict(), status.HTTP_201_CREATED)


@router.get('/get_task_status', response_model=TaskStatusModel)
@exception_handler
def get_task_status(id: str):
    """ Returns status of generation task with specified id """
    return api_utils.get_task_status(id)


@router.get('/get_tasks_statuses', response_model=typing.List[TaskStatusModel])
@exception_handler
def get_tasks_statuses(id: typing.List[str] = Query(None)):
    """ Returns status of generation for tasks with specified ids """
    results = get_celery_task_statuses(id)
    return results


@router.post('/revoke_tasks')
@exception_handler
def revoke_task(task: TaskIdsModel):
    """ Revokes celery task with specified id """
    api_utils.revoke_tasks(task.id)
    return JSONResponse({'result': 'Tasks successfully revoked.'})


@router.get('/get_task_result', response_model=TaskResultModel)
@exception_handler
def get_task_result(id: str):
    return JSONResponse(api_utils.get_task_result(id))


@router.get('/get_tasks_results', response_model=typing.List[TaskResultModel])
@exception_handler
def get_tasks_results(id: typing.List[str] = Query(None)):
    results = api_utils.get_celery_tasks_results(id)
    return JSONResponse(results)
