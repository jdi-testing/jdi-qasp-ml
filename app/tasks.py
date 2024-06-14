import datetime
import os

from lxml import etree, html

import app.mail_backend as backends
from app.celery_app import celery_app
from app.models import ReportMail, RobulaSettingsModel
from app.redis_app import redis_app
from utils.robula import generate_xpath
from .css_selectors import task_schedule_css_selectors_generation  # noqa: F401

ENV = os.getenv("ENV")


@celery_app.task(bind=True)
def task_schedule_xpath_generation(
    self,
    element_id: int,
    document_uuid: str,
    config: RobulaSettingsModel,
    session_id: int,
    website_url: str,
) -> str:
    start_time = datetime.datetime.utcnow()
    page = redis_app.get(document_uuid).decode("utf-8")
    result = generate_xpath(element_id, page, document_uuid, config)  # calculation itself

    # calculation of additional parameters if not locally
    if ENV != "LOCAL":
        end_time = datetime.datetime.utcnow()
        task_duration = end_time - start_time

        document = html.fromstring(page)
        element = document.xpath(element_id)[0]
        tree = etree.ElementTree(document)
        full_xpath = tree.getpath(element)
        nesting_num = len(full_xpath.split("/")) - 1

        task_kwargs = self.request.kwargs
        task_kwargs["task_duration"] = str(task_duration)  # for custom metrics logging to mongodb
        task_kwargs["start_time"] = str(start_time)  # for custom metrics logging to mongodb
        task_kwargs["full_xpath"] = full_xpath  # for custom metrics logging to mongodb
        task_kwargs["nesting_num"] = nesting_num  # for custom metrics logging to mongodb

    return result


@celery_app.task(
    bind=True,
    name="send_report_mail_task",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 10, "countdown": 60},
)
def send_report_mail_task(self, msg_content: ReportMail) -> int:
    for backend_callable in backends.mail_backend_list:
        backend_callable(msg_content)

    return -1
