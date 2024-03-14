from sqlalchemy import Boolean, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from config.db.base_crud import CRUDBase


class UserCRUD(CRUDBase):
    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        user = (await db.execute(select(cls).where(cls.email == email))).scalars().first()
        return user


class User(Base, UserCRUD):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    is_manager: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    basket_products = relationship("BasketProduct")
