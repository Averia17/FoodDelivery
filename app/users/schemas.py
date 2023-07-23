from typing import Optional

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True
