from app.celery import celery
from utils.robula import generate_xpath


@celery.task
def task_schedule_xpath_generation(element_id, document, config):
    return generate_xpath(element_id, document, config)
