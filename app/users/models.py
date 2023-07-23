from config.db import Base
from sqlalchemy import Column, String

from config.db.base_crud import CRUDBase


class User(Base, CRUDBase):
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String)
