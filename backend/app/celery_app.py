from celery import Celery
from .config import REDIS_URL, PULL_INTERVAL
import os

celery_app = Celery(
    "app",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"],  # Make sure tasks are loaded
)

# use schedule seconds as float
celery_app.conf.beat_schedule = {
    "pull-every-n-seconds": {
        "task": "app.tasks.pull_data_task",
        "schedule": PULL_INTERVAL,
    }
}
celery_app.conf.timezone = "UTC"
