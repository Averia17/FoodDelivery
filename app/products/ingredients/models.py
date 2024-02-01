from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.models import Product


class Ingredient(Base, CRUDBase):
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(
        secondary="productingredientassociation", back_populates="ingredients"
    )
