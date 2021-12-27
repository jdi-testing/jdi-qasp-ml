from app.celery_app import celery_app
from app.models import TaskStatusModel


def get_task_status(task_id):
    result = TaskStatusModel(id=task_id, status=celery_app.AsyncResult(task_id).status)
    return result


def get_task_result(task_id):
    result = celery_app.AsyncResult(task_id)
    if result.status == 'SUCCESS':
        return {'id': task_id, 'result': result.get()}
    else:
        return {'id': task_id, 'exc': 'Generation still in progress.'}


def get_xpath_from_id(element_id):
    """
    Returns xpath based on jdn_hash
    :param element_id:
    :return: xpath
    """
    return f"//*[@jdn-hash='{element_id}']"