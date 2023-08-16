from sqlalchemy.orm import relationship

from config.db import Base
from sqlalchemy import Column, String, Boolean
from config.db.base_crud import CRUDBase


class Category(Base, CRUDBase):
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    products = relationship("Product")
