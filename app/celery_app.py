from celery import Celery
from kombu import Queue

from app import REDIS_URL

celery_app = Celery(
    "app.main",
    broker=REDIS_URL,
    backend=REDIS_URL,
    task_track_started=True,
    task_default_queue="default",
    task_create_missing_queues=False,
    result_extended=True,
    task_queues=(
        Queue("default"),
        Queue("high_priority"),
        Queue("low_priority"),
    ),
)

celery_app.autodiscover_tasks(["app.tasks"], force=True)
