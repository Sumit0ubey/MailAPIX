from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
from os import getenv

load_dotenv()

USERNAME = getenv('DATABASE_USERNAME')
PASSWORD = getenv('DATABASE_PASSWORD')
HOSTNAME = getenv('DATABASE_HOSTNAME')
PORT = getenv('DATABASE_PORT')
NAME = getenv('DATABASE_NAME')

DATABASE_URL = f'postgresql+asyncpg://{USERNAME}:{PASSWORD}@{HOSTNAME}/{NAME}?ssl=require'

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
