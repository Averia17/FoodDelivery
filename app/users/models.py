from sqlalchemy.ext.asyncio import AsyncSession

from config.db import Base
from sqlalchemy import Column, String, Boolean, select

from config.db.base_crud import CRUDBase


class UserCRUD(CRUDBase):
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        user = (await db.execute(select(cls).where(cls.email == email))).scalars().first()
        return user


class User(Base, UserCRUD):
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String)
    is_manager = Column(Boolean, nullable=False, default=False)
    password = Column(String, nullable=False)
