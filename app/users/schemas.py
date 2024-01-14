import re
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class UserSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    phone_number: str
    full_name: Optional[str] = None
    is_manager: Optional[bool] = False

    class Config:
        from_attributes = True

    @field_validator("phone_number")
    @classmethod
    def validate_correct_format(cls, phone_number: str):
        if not re.match(r"^\+375(17|29|33|44)[0-9]{7}", phone_number):
            raise ValueError("Invalid phone number")
        return phone_number


class UserCreateSchema(UserSchema):
    password: str


class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_manager: Optional[bool] = False
