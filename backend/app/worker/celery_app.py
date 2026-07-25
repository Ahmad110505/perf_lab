from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "calculate-dashboard-summaries-daily": {
            "task": "app.worker.tasks.calculate_dashboard_summaries",
            "schedule": crontab(hour=0, minute=0),
        },
    }
)

celery_app.autodiscover_tasks(["app.worker.tasks"])
