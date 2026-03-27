from os import getenv

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

celery_kwargs = {
    "broker": CELERY_BROKER_URL,
    "include": ["MailApixAPI.Tasks.revoke_token_tasks"],
}

if CELERY_RESULT_BACKEND:
    celery_kwargs["backend"] = CELERY_RESULT_BACKEND

celery_app = Celery("mailapix", **celery_kwargs)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_ignore_result=True,
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

