import asyncio
from os import getenv
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Header, Depends, Query

from EmailServiceAPI.Controller.schema import EmailSchema, EmailWithPasskey
from EmailServiceAPI.Services.EmailService import EmailService
from EmailServiceAPI.Services.UserServices import UserService
from EmailServiceAPI.Controller.database import get_db
from EmailServiceAPI.utils import get_email_service

load_dotenv()

EMAIL = getenv('SYSTEM_EMAIL')
PASSKEY = getenv('SYSTEM_EMAIL_PASSKEY')

router = APIRouter(prefix="/email", tags=["Email_Service"])

def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def sendEmail(email: EmailWithPasskey, token: str = Header(...), service: UserService = Depends(get_user_service),
                    company_name: str = None, company_link: str = None, email_title: str = None, template_id: int = Query(0, ge=0, le=4)):
    user = await service.get_user_by_token(token)
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    if user.numberOfEmailSend > user.numberOfEmailCanSend:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Maximum quota exceeded"})

    custom_html = email.customHtml if template_id == 4 else None

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_mail(
            username=user.email,
            password=email.passKey,
            to=email.sendTo,
            subject=email_title,
            data=email.content,
            template_id=template_id,
            custom_html=custom_html,
            company_name=company_name,
            company_link=company_link,
            email_title=email.title,
            timeout=30,
            text_fallback=email.content,
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email...\n Check your credential and try again."})

    await service.update_email_send_count(user)

    content = {
        "Message": f"Email send to {email.sendTo} with tile {email.title} using {get_email_service(user.email)} service"}

    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)


@router.post("/default", status_code=status.HTTP_202_ACCEPTED)
async def defaultEmailService(email: EmailSchema, token: str = Header(...), service: UserService = Depends(get_user_service),
                              company_name: str = None, company_link: str = None, email_title: str = None, template_id: int = Query(0, ge=0, le=4)):
    user = await service.get_user_by_token(token)
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized Access"})

    if user.numberOfEmailSend >= user.numberOfEmailCanSend or user.defaultEmailTimeUsed >= user.defaultEmailTimeCanUsed:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Maximum quota exceeded"})

    custom_html = email.customHtml if template_id == 4 else None

    is_email_send = await asyncio.to_thread(
        lambda: EmailService.send_mail(
            username=EMAIL,
            password=PASSKEY,
            to=user.email,
            subject=email_title,
            template_id=template_id,
            data=email.content,
            custom_html=custom_html,
            company_name=company_name,
            company_link=company_link,
            email_title=email.title,
            timeout=30,
            text_fallback=email.content,
        )
    )

    if not is_email_send:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Failed to send email... Check your credential and try again."})

    await service.update_default_email_send_count(user)

    content = {
        "Message": f"Email send to {email.sendTo} with tile {email.title} using Gmail service"}

    return JSONResponse(content=content, status_code=status.HTTP_202_ACCEPTED)
