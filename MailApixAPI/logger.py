import logging
from os import getenv

try:
    from celery.utils.log import get_task_logger as celery_get_task_logger
except Exception:
    celery_get_task_logger = None


class LoggerFactory:
    _configured = False

    @classmethod
    def configure(cls) -> None:
        if cls._configured:
            return

        level_name = getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        root = logging.getLogger()

        if not root.handlers:
            logging.basicConfig(
                level=level,
                format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                handlers=[logging.StreamHandler()],
            )
        else:
            root.setLevel(level)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        cls.configure()
        return logging.getLogger(name)

    @classmethod
    def get_task_logger(cls, name: str) -> logging.Logger:
        cls.configure()
        if celery_get_task_logger:
            return celery_get_task_logger(name)
        return logging.getLogger(name)

