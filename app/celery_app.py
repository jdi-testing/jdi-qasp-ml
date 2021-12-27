from celery import Celery

from app import REDIS_URL

celery_app = Celery("app.main", broker=REDIS_URL, backend=REDIS_URL, task_track_started=True)
celery_app.autodiscover_tasks(['app.tasks'], force=True)
