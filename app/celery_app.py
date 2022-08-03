from celery import Celery

import kombu_redis_priority.transport.redis_priority_async  # noqa
from app import REDIS_BROKER, REDIS_BACKEND

celery_app = Celery(
    "app.main",
    broker=REDIS_BROKER,
    backend=REDIS_BACKEND,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_extended=True
)
celery_app.autodiscover_tasks(["app.tasks"], force=True)
