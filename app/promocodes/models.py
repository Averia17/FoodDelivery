import datetime
from typing import TYPE_CHECKING, Annotated

from fastapi.params import Path
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.product_variants.models import ProductVariant


class PromoCodeCRUD(CRUDBase):
    @classmethod
    async def get_by_promo_code_id(cls, db: AsyncSession, promo_code_id: str):
        promo_code = await db.scalar(
            select(PromoCode).where(PromoCode.id == promo_code_id).options(selectinload(PromoCode.product_variants))
        )
        return promo_code


class PromoProductAssociation(Base, CRUDBase):
    __table_args__ = (UniqueConstraint("promo_code_id", "product_variant_id", name="idx_unique_promo_product"),)

    promo_code_id = mapped_column(String, ForeignKey("promo_code.id", ondelete="CASCADE"), nullable=False)
    product_variant_id = mapped_column(Integer, ForeignKey("product_variant.id", ondelete="CASCADE"), nullable=False)


class PromoCode(Base, PromoCodeCRUD):
    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True, unique=True)
    valid_from: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.UTC)
    )
    valid_until: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    discount: Mapped[Annotated[int, Path(ge=1, lt=100)]] = mapped_column(nullable=True, default=0)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    product_variants: Mapped[list["ProductVariant"]] = relationship(
        secondary="promo_product_association", back_populates="promo_codes"
    )
