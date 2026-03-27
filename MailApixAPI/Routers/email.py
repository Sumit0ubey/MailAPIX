import asyncio
from os import getenv
from textwrap import dedent

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, status, Header, Depends, Query

from MailApixAPI.Controller.schema import EmailSchema, EmailWithPasskey
from MailApixAPI.Services.EmailService import EmailService
from MailApixAPI.Services.UserServices import UserService
from MailApixAPI.Controller.database import get_db
from MailApixAPI.utils import get_email_service

load_dotenv()

EMAIL = getenv('SYSTEM_EMAIL')
PASSKEY = getenv('SYSTEM_EMAIL_PASSKEY')

router = APIRouter(prefix="/email", tags=["Email_Service"])

def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)

@router.post(
    "/",
    summary="Sends email",
    description=dedent("""
    Sends an email using authenticated user's SMTP credentials.
    
    **Required headers**
    - `token`: user's current token
    
    **Optional headers**
    - `email title`: Title that appears on the inbox (Email Subject)
    - `Template id`: Templates for sending email (more detail at the end)
    - `Company name`: Company name
    - `Company link`: Company link
    
    **Required Body Parameters**
    - `Title`: Email Title
    - `content`: Email content
    - `sendTo`: Email address of the recipient
    - `passKey`: Password of the email (usually App Password)
    
    **Optional Body Parameters**
    - `customHtml`: Instead of template id user can pass their own
    
    **Limits**
    - quota checks are applied
    
    **TEMPLATES**
    - `Range`: Template id ranges from 0 to 4
    - `0`: For simple text based email (no html)
    - `1 - 3`: Pre-defined html templates
    - `4`: For if user providing custom html  
    
    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202:{"description":"Email send successfully"},
        401:{"description":"Unauthorized access"},
        403:{"description": "Maximum quota exceeded"},
        500:{"description":"Internal Server Error"}
    }
)
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


@router.post(
    "/default",
    summary="Sends Email",
    description=dedent("""
     Sends an email using system mail.
    
    **Required headers**
    - `token`: user's current token
    
    **Optional headers**
    - `email title`: Title that appears on the inbox (Email Subject)
    - `Template id`: Templates for sending email (more detail at the end)
    - `Company name`: Company name
    - `Company link`: Company link
    
    **Required Body Parameters**
    - `Title`: Email Title
    - `content`: Email content
    - `sendTo`: Email address of the recipient
    
    **Optional Body Parameters**
    - `customHtml`: Instead of template id user can pass their own
    
    **Limits**
    - quota checks are applied
    
    **TEMPLATES**
    - `Range`: Template id ranges from 0 to 4
    - `0`: For simple text based email (no html)
    - `1 - 3`: Pre-defined html templates
    - `4`: For if user providing custom html  
    
    """),
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202:{"description":"Email send successfully"},
        401:{"description":"Unauthorized access"},
        403:{"description": "Maximum quota exceeded"},
        500:{"description":"Internal Server Error"}
    }
)
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
            to=email.sendTo,
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
