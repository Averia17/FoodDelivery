from typing import TYPE_CHECKING

from sqlalchemy import (
    DECIMAL,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.selectable import Select

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.categories.models import Category
    from products.ingredients.models import Ingredient


class ProductIngredientAssociation(Base, CRUDBase):
    __table_args__ = (UniqueConstraint("ingredient_id", "product_id", name="idx_unique_ingredient_product"),)

    ingredient_id = Column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)


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

    category: Mapped["Category"] = relationship(back_populates="products")
    ingredients: Mapped[list["Ingredient"]] = relationship(
        secondary="productingredientassociation", back_populates="products"
    )
