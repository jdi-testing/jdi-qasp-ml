from app.celery_app import celery_app


@celery_app.task(bind=True)
def task_schedule_css_locator_generation(self, element_id: int, document_uuid: str) -> str:
    ...
