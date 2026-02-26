from sqlalchemy import and_
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from MailApixAPI.utils import generate_key, hash_password, verify_password
from MailApixAPI.Controller.schema import CreateUserSchema
from MailApixAPI.Controller.models import User


class UserService:

    def __init__(self, db: AsyncSession):
        self.db : AsyncSession = db


    async def create_user(self, new_user : CreateUserSchema) -> bool|User|None:
        new_key = generate_key()

        existing_user = await self.db.scalar(
            select(User).where(User.email == new_user.email)
        )

        if existing_user:
            return False

        new_user = User(
            apiToken=new_key,
            password=hash_password(""),
            **new_user.model_dump()
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user


    async def get_user(self, user_id: str) -> User|None:
        return await self.db.scalar(
            select(User).where(User.id == user_id)
        )


    async def get_user_details_by_id(self, user_id: str) -> User|None:
        return await self.db.scalar(
            select(User).where(User.id == user_id)
        )

    async def get_user_by_token(self, token: str) -> User|None:
        return await self.db.scalar(
            select(User).where(User.apiToken == token)
        )


    async def update_user_token(self, user_id: str, token: str, password: str = "") -> bool|User|None :
        user = await self.db.scalar(
            select(User).where(
                and_(
                    User.id == user_id,
                    User.apiToken == token
                )
            )
        )

        if not user:
            return None

        if not verify_password(password, user.password):
            return False

        new_token = generate_key(24)
        user.apiToken = new_token

        await self.db.commit()
        await self.db.refresh(user)

        return user


    async def update_set_password(self, user_id: str, email: EmailStr, token: str, new_password: str = "", old_password: str = "") -> bool|User|None :
        user = await self.db.scalar(
            select(User).where(
                and_(
                    User.id == user_id,
                    User.apiToken == token,
                    User.email == email
                )
            )
        )

        if not user:
            return None

        if not verify_password(old_password, user.password):
            return False

        user.password = hash_password(new_password)

        await self.db.commit()
        await self.db.refresh(user)

        return user


    async def update_default_email_send_count(self, user: User):
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                defaultEmailTimeUsed=User.defaultEmailTimeUsed + 1
            )
        )

        await self.db.commit()


    async def update_email_send_count(self, user: User):
        await self.db.execute(
            update(User)
            .where(User.id == user.id)
            .values(
                numberOfEmailSend=User.numberOfEmailSend + 1
            )
        )

        await self.db.commit()

