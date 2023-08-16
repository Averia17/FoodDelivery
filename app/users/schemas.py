from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_manager: Optional[bool] = False

    class Config:
        from_attributes = True


class UserCreateSchema(UserSchema):
    password: str


class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_manager: Optional[bool] = False
