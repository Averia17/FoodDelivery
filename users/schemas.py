from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
