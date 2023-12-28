from sqlalchemy.ext.asyncio import AsyncSession

from config.db import Base
from sqlalchemy import Column, String, Boolean, Integer, Text, DECIMAL, ForeignKey
from sqlalchemy.sql.selectable import Select
from config.db.base_crud import CRUDBase


class ProductCRUD(CRUDBase):
    @classmethod
    async def filter(cls, db: AsyncSession, query: Select):
        return (await db.execute(query)).scalars().all()


class Product(Base, ProductCRUD):
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    description = Column(Text)
    discount = Column(Integer)
    price = Column(DECIMAL, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
