from typing import TYPE_CHECKING, Annotated

from fastapi.params import Path
from sqlalchemy import ForeignKey, UniqueConstraint, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship, selectinload

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.product_variants.models import ProductVariant
    from users.models import User


class BasketProductCRUD(CRUDBase):
    @classmethod
    async def get_by_user_id(cls, db: AsyncSession, user_id: int):
        basket_products = await db.scalars(
            select(BasketProduct)
            .where(BasketProduct.user_id == user_id)
            .options(joinedload(BasketProduct.user))
            .options(selectinload(BasketProduct.product_variant))
        )
        return basket_products


class BasketProduct(Base, BasketProductCRUD):
    __table_args__ = (UniqueConstraint("user_id", "product_variant_id", name="idx_unique_user_basket_product"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variant.id", ondelete="CASCADE"), nullable=False
    )
    count: Mapped[Annotated[int, Path(ge=1)]] = mapped_column(nullable=False, default=1)

    user: Mapped["User"] = relationship(back_populates="basket_products")
    product_variant: Mapped["ProductVariant"] = relationship(back_populates="basket_product")
