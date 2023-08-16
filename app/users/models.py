from config.db import Base
from sqlalchemy import Column, String, Boolean

from config.db.base_crud import UserCRUD


class User(Base, UserCRUD):
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String)
    is_manager = Column(Boolean, nullable=False, default=False)
    password = Column(String, nullable=False)
