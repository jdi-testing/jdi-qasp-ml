from main import celery
from utils.robula import generate_xpath


@celery.task
def schedule_xpath_generation(element_id, document, config):
    return generate_xpath(element_id, document, config)
