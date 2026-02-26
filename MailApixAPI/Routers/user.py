import asyncio
from os import getenv
from textwrap import dedent

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Header, Depends

from MailApixAPI.Controller.schema import CreateUserSchema, GetUserSchema, SecureAccount
from MailApixAPI.Services.EmailService import EmailService
from MailApixAPI.Services.UserServices import UserService
from MailApixAPI.Controller.schema import Password
from MailApixAPI.Controller.database import get_db

load_dotenv()

EMAIL = getenv('SYSTEM_EMAIL')
PASSKEY = getenv('SYSTEM_EMAIL_PASSKEY')

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
            subject="Welcome to MailApix API - Registration Successful",
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
        apiToken=user.apiToken,
        isPaidUser=user.isPaidUser,
        numberOfEmailSend=user.numberOfEmailSend,
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
    "/newToken/{id}",
    summary="Generates new token",
    description=dedent("""
    Generates new token and send it's to the user's mail.
    
    **Required headers**
    - `user id`: user's id
    - `token`: user's current token
    
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
async def newToken(user_id: str, password: Password, token: str = Header(...), service: UserService = Depends(get_user_service)):
    user = await service.update_user_token(user_id=user_id, token=token, password=password.password)

    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_system_mail(
            username=EMAIL,
            password=PASSKEY,
            to=user.email,
            subject="MailApix API - Token Changed Successful",
            system_template="tokenrevert",
            token=user.apiToken
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email"})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"Message": "We have send you an email with your new token please check it.."})


@router.put(
    "/secureAccount{id}",
    summary="Sets account password",
    description=dedent("""
    Sets new account password.
    
    **Required headers**
    - `user id`: user's id
    - `token`: user's current token
    
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
async def setPassword(user_id: str, data: SecureAccount, token: str = Header(...), service: UserService = Depends(get_user_service)):
    if data.setPassword != data.confirmPassword:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"message": "Password does not match"})

    user = await service.update_set_password(
        user_id=user_id,
        email=data.email,
        token=token,
        new_password=data.setPassword,
        old_password=data.oldPassword
    )

    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Now your Account is Secure | Password is set"})
