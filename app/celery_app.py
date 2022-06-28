from celery import Celery

from app import REDIS_URL

celery_app = Celery(
    "app.main",
    broker=REDIS_URL,
    backend=REDIS_URL,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
celery_app.autodiscover_tasks(["app.tasks"], force=True)
