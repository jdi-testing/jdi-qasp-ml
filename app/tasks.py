from app.celery_app import celery_app
from utils.robula import generate_xpath


@celery_app.task
def task_schedule_xpath_generation(element_id, document, config):
    return generate_xpath(element_id, document, config)
