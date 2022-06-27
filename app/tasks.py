import app.mail_backend as backends
from app.celery_app import celery_app
from utils.robula import generate_xpath


@celery_app.task
def task_schedule_xpath_generation(element_id, document, config):
    return generate_xpath(element_id, document, config)


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
