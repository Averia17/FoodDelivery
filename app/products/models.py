from sqlalchemy.ext.asyncio import AsyncSession

from config.db import Base
from sqlalchemy import Column, String, Boolean, Integer, Text, DECIMAL, ForeignKey, select
from config.db.base_crud import CRUDBase


class ProductCRUD(CRUDBase):
    @classmethod
    async def get_by_category(cls, db: AsyncSession, category_id: int):
        products = (await db.execute(select(cls).where(cls.category_id == category_id))).scalars().all()
        return products

    @classmethod
    async def get_by_price(cls, db: AsyncSession, price: float):
        products = (await db.execute(select(cls).where(cls.price <= price))).scalars().all()
        return products

    @classmethod
    async def get_by_category_and_price(cls, db: AsyncSession, category_id: int, price: float):
        products = (
            (await db.execute(select(cls).where(cls.category_id == category_id).where(cls.price <= price)))
            .scalars()
            .all()
        )
        return products


class Product(Base, ProductCRUD):
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    description = Column(Text)
    discount = Column(Integer)
    price = Column(DECIMAL, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
