import asyncio
from os import getenv
from textwrap import dedent

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Header, Depends, Path

from MailApixAPI.Controller.schema import CreateUserSchema, GetUserSchema, SecureAccount
from MailApixAPI.Services.EmailService import EmailService
from MailApixAPI.Services.UserServices import UserService
from MailApixAPI.Tasks.revoke_token_tasks import invalidate_revoke_token
from MailApixAPI.logger import LoggerFactory
from MailApixAPI.Controller.schema import Password
from MailApixAPI.Controller.database import get_db

load_dotenv()

EMAIL = getenv('SYSTEM_EMAIL')
PASSKEY = getenv('SYSTEM_EMAIL_PASSKEY')
REVOKE_KEY_TTL = int(getenv('REVOKE_KEY_TTL', 240))

logger = LoggerFactory.get_logger(__name__)

router = APIRouter(prefix="/users", tags=["User"])

def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

@router.post(
    "/",
    summary="User Registration",
    description=dedent("""
    Register a new user.
    
    **Required headers**
    - `Full Name`: user's full name
    - `Email`: user's email
    
    """),
    status_code=status.HTTP_201_CREATED,
    responses={
        201:{"description": "User Registration Successful"},
        404:{"description": "User cannot be created or email already exists"},
        500:{"description": "Internal Server Error"},
    }
)
async def register(user: CreateUserSchema, service: UserService = Depends(get_user_service)):
    new_user = await service.create_user(user)

    if not new_user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User cannot be created or email already exists"})

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_system_mail(
            username=EMAIL,
            password=PASSKEY,
            to=new_user.email,
            subject="Welcome to MailApix - Registration Successful",
            system_template="registration",
            data="",
            iD=new_user.id,
            token=new_user.apiToken
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email"})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "We have send your credential to your email. please check it.."})


@router.get(
    "/info",
    summary="User Info",
    description=dedent("""
    Gives the information of the user.
    
    **Required headers**
    - `user id`: user's id
    
    """),
    status_code=status.HTTP_302_FOUND,
    response_model=GetUserSchema,
    responses={
        302:{"description": "User Info fetched successfully"},
        404:{"description":"User does not exists"}
    }
)
async def info(user_id: str = Header(...), service: UserService = Depends(get_user_service)):

    user = await service.get_user_details_by_id(user_id)

    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User does not exists"})

    return GetUserSchema(
        id=user.id,
        fullName=user.fullName,
        email=user.email,
        isPaidUser=user.isPaidUser,
        numberOfEmailSend=user.numberOfEmailSend,
        numberOfEmailCanSend=user.numberOfEmailCanSend,
        numberOfDefaultEmailSend=user.defaultEmailCanSend,
        numberOfDefaultEmailCanSend=user.defaultEmailCanSend,
        createdAt=user.createdAt
    )


@router.get(
    "/upgrade",
    summary="User Upgrade Plan",
    description=dedent("""
    Sends Upgrade Plan Email to the user.
    
    **Required headers**
    - `user id`: user's id
    
    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202:{"description":"Upgrade plan send successfully"},
        404:{"description":"User does not exists"},
        505:{"description":"Internal Server Error"}
    }
)
async def becomePaidUser(user_id: str = Header(...), service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)

    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "User does not exists"})

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_system_mail(
            username=EMAIL,
            password=PASSKEY,
            to=user.email,
            subject="Your Upgrade Plan - increase your email quota",
            system_template="packages"
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email"})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"Message": "We have send you an email please check it.."})


@router.post(
    "/revokeKey/{id}",
    summary="Generates Revoke key",
    description=dedent(f"""
    Generates Revoke Key, valid for {int(REVOKE_KEY_TTL/60)} Minutes.

    **Required path parameter**
    - `id`: user's id

    **Optional Body Parameters**
    - `password`: user's password (if set any else leave it)

    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"description": "Revoke Key Generated Successfully"},
        401: {"description": "Unauthorized Access"},
        503: {"description": "Queue Service Unavailable"},
        500: {"description": "Internal Server Error"}
    }
)
async def revokeToken(id: str = Path(...), password: Password = ..., service: UserService = Depends(get_user_service)):
    user = await service.update_revoke_token(user_id=id, password=password.password)

    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_system_mail(
            username=EMAIL,
            password=PASSKEY,
            to=user.email,
            subject="MailApix - Revoke Key",
            system_template="revoke_token",
            token=user.revokeToken,
        )
    )

    if not is_email_send:
        logger.error("[revoke-email] failed to send revoke email user_id=%s email=%s", user.id, user.email)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send revoke email"})

    try:
        invalidate_task = invalidate_revoke_token.apply_async(
            args=[user.id, user.revokeToken],
            countdown=REVOKE_KEY_TTL,
        )
    except Exception:
        await service.invalidate_revoke_token(user_id=user.id, expected_revoke_token=user.revokeToken)
        logger.exception("[revoke-queue] failed to publish invalidate task user_id=%s", user.id)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"message": "Revoke email sent, but auto-expiry scheduling failed. Please generate a new revoke key."},
        )

    logger.info(
        "[revoke-queue] revoke email sent and invalidate task queued user_id=%s invalidate_task_id=%s ttl_seconds=%s",
        user.id,
        invalidate_task.id,
        REVOKE_KEY_TTL,
    )

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                        content={
                            "message": f"Revoke key email sent. The key will auto-expire in {int(REVOKE_KEY_TTL/60)} minutes.",
                            "invalidateTaskId": invalidate_task.id,
                        })


@router.post(
    "/newToken/{id}",
    summary="Generates new token",
    description=dedent("""
    Generates new token and send it's to the user's mail.
    
    **Required path parameter**
    - `id`: user's id
    - `key`: revoke Key
    
    **Optional Body Parameters**
    - `password`: user's password (if set any else leave it)
    
    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202:{"description":"New Token Generated Successfully"},
        401:{"description":"Unauthorized Access"},
        500:{"description":"Internal Server Error"}
    }
)
async def newToken(id: str = Path(...), password: Password = ..., key: str = Header(...), service: UserService = Depends(get_user_service)):
    user = await service.update_user_token(user_id=id, token=key, password=password.password)

    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_system_mail(
            username=EMAIL,
            password=PASSKEY,
            to=user.email,
            subject="MailApix - Token Changed Successful",
            system_template="tokenrevert",
            token=user.apiToken
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email"})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"Message": "We have send you an email with your new token please check it.."})


@router.put(
    "/secureAccount/{id}",
    summary="Sets account password",
    description=dedent("""
    Sets new account password.
    
    **Required path parameter**
    - `id`: user's id
    - `key`: revoke key
    
    **Optional Body Parameters**
    - `old password`: old password (if set any else leave it)
    
    **Required Body Parameters**
    - `new password`: new password
    - `confirm password`: re-enter the same new password here
    
    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202:{"description":"New Password Set Successfully"},
        401:{"description":"Unauthorized Access"},
        409:{"description":"New & Confirm Password does not match"},
        500:{"description":"Internal Server Error"}
    }
)
async def setPassword(id: str = Path(...), data: SecureAccount = ..., key: str = Header(...), service: UserService = Depends(get_user_service)):
    if data.setPassword != data.confirmPassword:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Password does not match"})

    user = await service.update_set_password(
        user_id=id,
        email=data.email,
        token=key,
        new_password=data.setPassword,
        old_password=data.oldPassword
    )

    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Now your Account is Secure | Password is set"})
