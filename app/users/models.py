from sqlalchemy.ext.asyncio import AsyncSession

from config.db import Base
from sqlalchemy import Column, String, select

from config.db.base_crud import CRUDBase


class User(Base, CRUDBase):
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String)
    password = Column(String, nullable=False)

    @classmethod
    async def get_user_by_email(cls, db: AsyncSession, email: str):
        user = (await db.execute(select(cls).where(cls.email == email))).scalars().first()
        return user
