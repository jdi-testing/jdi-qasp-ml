import concurrent.futures
import json
import os

from flask import request

from main import api, celery
from utils import api_utils, robula
import tasks


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return api_utils.get_json_response({'exc': str(e)}, 500)

    wrapper.__name__ = func.__name__
    return wrapper


@api.route('/generate_xpath', methods=['POST'])
def generate_xpath():
    data = json.loads(request.data)

    page = json.loads(data['document'])
    config = get_robula_config(data)
    ids = list(set(data['ids']))

    result = generate_xpaths_simultaneously(ids, config, page)

    return api_utils.get_json_response(result, 200)


@api.route('/schedule_xpath_generation', methods=['POST'])
@exception_handler
def schedule_xpath_generation():
    """ Creates new celery task for xpath generation. Returns celery task id """
    data = json.loads(request.data)

    page = json.loads(data['document'])
    config = get_robula_config(data)
    element_id = data['id']

    task_result = tasks.schedule_xpath_generation.delay(get_xpath_from_id(element_id), page, config)
    result = {'task_id': task_result.id}
    return api_utils.get_json_response(result, 200)


@api.route('/get_task_status', methods=['POST'])
@exception_handler
def get_task_status():
    """ Returns status of generation task with specified id """
    task_id = json.loads(request.data)['id']
    return api_utils.get_json_response(api_utils.get_task_status(task_id), 200)


@api.route('/get_tasks_statuses', methods=['POST'])
@exception_handler
def get_tasks_statuses():
    """ Returns status of generation for tasks with specified ids """
    task_ids = json.loads(request.data)['id']

    results = []
    for id in task_ids:
        results.append(api_utils.get_task_status(id))
    return api_utils.get_json_response(results, 200)


@api.route('/revoke_task', methods=['POST'])
@exception_handler
def revoke_task():
    """ Revokes celery task with specified id """
    task_id = json.loads(request.data)['id']
    celery.control.revoke(task_id, terminate=True, signal='SIGKILL')
    return api_utils.get_json_response({'result': 'Task successfully revoked.'}, 200)


@api.route('/get_task_result', methods=['POST'])
@exception_handler
def get_task_result():
    task_id = json.loads(request.data)['id']
    return api_utils.get_json_response(api_utils.get_task_result(task_id), 200)


@api.route('/get_tasks_results', methods=['POST'])
@exception_handler
def get_tasks_results():
    task_ids = json.loads(request.data)['id']

    results = []
    for task_id in task_ids:
        results.append(api_utils.get_task_result(task_id))
    return api_utils.get_json_response(results, 200)


def get_robula_config(data):
    config = robula.get_default_config()
    try:
        config.update(data['config'])
    except KeyError:
        pass
    return config


def generate_xpaths_simultaneously(ids, config, page):
    result = {}
    workers = min(os.cpu_count(), len(ids))
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as pool:
        future_to_xpath = {pool.submit(robula.generate_xpath, get_xpath_from_id(id), page, config): id for id in ids}
        for future in concurrent.futures.as_completed(future_to_xpath):
            element_id = future_to_xpath[future]
            try:
                result[element_id] = future.result()
            except Exception as exc:
                api.logger.info('%r generated an exception: %s' % (element_id, exc))
    return result


def get_xpath_from_id(element_id):
    """
    Returns xpath based on jdn_hash
    :param element_id:
    :return: xpath
    """
    return f"//*[@jdn-hash='{element_id}']"
