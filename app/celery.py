from celery import Celery

from app import REDIS_URL
from app.main import api

celery = Celery(api.name, broker=REDIS_URL, backend=REDIS_URL, task_track_started=True)
celery.autodiscover_tasks(['app.tasks'], force=True)
