from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.db import Base
from config.db.base_crud import CRUDBase

if TYPE_CHECKING:
    from products.models import Product


class Category(Base, CRUDBase):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")
