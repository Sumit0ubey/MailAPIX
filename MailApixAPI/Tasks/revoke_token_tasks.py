import asyncio

from MailApixAPI.celery_app import celery_app
from MailApixAPI.Controller.database import AsyncSessionLocal
from MailApixAPI.Services.UserServices import UserService
from MailApixAPI.logger import LoggerFactory

logger = LoggerFactory.get_task_logger(__name__)


async def _invalidate_revoke_token_async(user_id: str, expected_revoke_token: str) -> bool:
    async with AsyncSessionLocal() as session:
        service = UserService(session)
        is_invalidated = await service.invalidate_revoke_token(
            user_id=user_id,
            expected_revoke_token=expected_revoke_token,
        )
        logger.info("[revoke-invalidate] DB update result user_id=%s invalidated=%s", user_id, is_invalidated)
        return is_invalidated


def _run_invalidate_task(user_id: str, expected_revoke_token: str) -> bool:
    logger.info("[revoke-invalidate] task started user_id=%s", user_id)
    try:
        is_invalidated = asyncio.run(_invalidate_revoke_token_async(user_id, expected_revoke_token))
        logger.info("[revoke-invalidate] task finished user_id=%s invalidated=%s", user_id, is_invalidated)
        return is_invalidated
    except Exception:
        logger.exception("[revoke-invalidate] task failed user_id=%s", user_id)
        return False


@celery_app.task(name="mailapix.invalidate_revoke_token")
def invalidate_revoke_token(user_id: str, expected_revoke_token: str) -> bool:
    return _run_invalidate_task(user_id, expected_revoke_token)


@celery_app.task(name="MailApixAPI.Tasks.revoke_token_tasks.invalidate_revoke_token")
def invalidate_revoke_token_compat(user_id: str, expected_revoke_token: str) -> bool:
    return _run_invalidate_task(user_id, expected_revoke_token)


