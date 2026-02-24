from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
import uuid

from EmailServiceAPI.Controller.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fullName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    apiToken = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False, server_default=text("''"))
    isPaidUser = Column(Boolean, nullable=False, server_default=text('false'))
    numberOfEmailSend = Column(Integer, nullable=False, server_default=text("0"))
    numberOfEmailCanSend = Column(Integer, nullable=False, server_default=text("20"))
    defaultEmailTimeUsed = Column(Integer, nullable=False, server_default=text("0"))
    defaultEmailTimeCanUsed = Column(Integer, nullable=False, server_default=text("5"))
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
