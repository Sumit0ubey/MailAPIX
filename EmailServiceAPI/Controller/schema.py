from pydantic import BaseModel, EmailStr, field_serializer
from typing import Optional, Iterable, Union
from datetime import datetime

from EmailServiceAPI.utils import serialize_timestamp


class CreateUserSchema(BaseModel):
    fullName: str
    email: EmailStr


class GetUserSchema(BaseModel):
    id: str
    fullName: str
    email: EmailStr
    apiToken: str
    isPaidUser: bool
    numberOfEmailSend: int
    createdAt: datetime

    @field_serializer("createdAt")
    def timestampSerializer(self, dt: datetime) -> str:
        return serialize_timestamp(dt)

    class Config:
        from_attributes = True


class EmailSchema(BaseModel):
    title: str
    content: str
    sendTo: Union[str, Iterable[str]]
    customHtml: Optional[str] = None


class EmailWithPasskey(EmailSchema):
    passKey: str


class SecureAccount(BaseModel):
    email: EmailStr
    oldPassword: Optional[str] = ""
    setPassword: str
    confirmPassword: str

    class Config:
        from_attributes = True


class Password(BaseModel):
    password: Optional[str] = ""
