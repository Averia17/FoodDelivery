from config.db import Base
from sqlalchemy import Column, String

from config.db.base_crud import UserCRUD


class User(Base, UserCRUD):
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String)
    password = Column(String, nullable=False)
