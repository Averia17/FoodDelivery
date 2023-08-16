from sqlalchemy.orm import relationship

from config.db import Base
from sqlalchemy import Column, String, Boolean, Integer, Text, DECIMAL, ForeignKey
from config.db.base_crud import ProductCRUD


class Product(Base, ProductCRUD):
    name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    description = Column(Text)
    discount = Column(Integer)
    price = Column(DECIMAL, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
