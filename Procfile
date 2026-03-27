web: gunicorn -k uvicorn.workers.UvicornWorker MailApixAPI.main:app
worker: celery -A MailApixAPI.celery_app:celery_app worker --loglevel=info
