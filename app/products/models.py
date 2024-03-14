from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship, selectinload
from sqlalchemy.sql.selectable import Select

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.categories.models import Category
    from products.ingredients.models import Ingredient
    from products.product_variants.models import ProductVariant


class ProductIngredientAssociation(Base, CRUDBase):
    __table_args__ = (UniqueConstraint("ingredient_id", "product_id", name="idx_unique_ingredient_product"),)

    ingredient_id = Column(Integer, ForeignKey("ingredient.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)


class ProductCRUD(CRUDBase):
    @classmethod
    async def filter(cls, db: AsyncSession, query: Select):
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int):
        product = await db.scalar(
            select(Product)
            .where(Product.id == id)
            .options(joinedload(Product.category))
            .options(selectinload(Product.ingredients))
        )
        return product


class Product(Base, ProductCRUD):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    discount: Mapped[int] = mapped_column(Integer, nullable=True)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))

    category: Mapped["Category"] = relationship(back_populates="products")
    ingredients: Mapped[list["Ingredient"]] = relationship(
        secondary="product_ingredient_association", back_populates="products"
    )
    product_variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product")
