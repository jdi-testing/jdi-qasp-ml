from celery import Celery

import kombu_redis_priority.transport.redis_priority_async  # noqa
from app import REDIS_URL

celery_app = Celery(
    "app.main",
    broker="redispriorityasync://redis:6379",
    backend=REDIS_URL,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
celery_app.autodiscover_tasks(["app.tasks"], force=True)
