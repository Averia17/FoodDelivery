from typing import TYPE_CHECKING, Annotated

from fastapi.params import Path
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.models import Product
    from promocodes.models import PromoCode


class ProductVariant(Base, CRUDBase):
    __table_args__ = (UniqueConstraint("product_id", "weight", name="idx_unique_product_weight"),)

    # TODO: add names which is like CHOICES in django
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[Annotated[int, Path(gt=0)]] = mapped_column(nullable=False, comment="Price in kopecks")
    discount: Mapped[Annotated[int, Path(ge=0, lt=100)]] = mapped_column(nullable=True, default=0)
    weight: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship(back_populates="product_variants")
    basket_product = relationship("BasketProduct")
    promo_codes: Mapped[list["PromoCode"]] = relationship(
        secondary="promo_product_association", back_populates="product_variants"
    )
