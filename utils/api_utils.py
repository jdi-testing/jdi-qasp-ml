import json
from main import celery, api


def get_task_status(task_id):
    return {'id': task_id, 'status': celery.AsyncResult(task_id).status}


def get_task_result(task_id):
    result = celery.AsyncResult(task_id)
    if result.status == 'SUCCESS':
        return {'id': task_id, 'result': result.get()}
    else:
        return {'id': task_id, 'exc': 'Generation still in progress.'}


def get_json_response(body, status):
    response = api.response_class(
                response=json.dumps(body),
                status=status,
                mimetype='application/json'
            )
    return response
