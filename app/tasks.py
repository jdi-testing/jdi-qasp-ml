import datetime

from lxml import etree, html

import app.mail_backend as backends
from app.celery_app import celery_app
from utils.robula import generate_xpath


@celery_app.task(bind=True)
def task_schedule_xpath_generation(
    self, element_id, document, config, session_id, website_url
):
    start_time = datetime.datetime.utcnow()
    result = generate_xpath(element_id, document, config)
    end_time = datetime.datetime.utcnow()
    task_duration = end_time - start_time

    document = html.fromstring(document)
    element = document.xpath(element_id)[0]
    tree = etree.ElementTree(document)
    full_xpath = tree.getpath(element)
    nesting_num = len(full_xpath.split("/")) - 1

    task_kwargs = self.request.kwargs
    task_kwargs["task_duration"] = str(task_duration)
    task_kwargs["start_time"] = str(start_time)
    task_kwargs["full_xpath"] = full_xpath
    task_kwargs["nesting_num"] = nesting_num
    return result


@celery_app.task(
    bind=True,
    name="send_report_mail_task",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 10, "countdown": 60},
)
def send_report_mail_task(self, msg_content):
    for backend_callable in backends.mail_backend_list:
        backend_callable(msg_content)

    return -1
