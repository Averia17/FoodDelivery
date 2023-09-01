from typing import Optional

from pydantic import BaseModel


class CategorySchema(BaseModel):
    id: Optional[int] = None
    is_active: Optional[bool] = True
    name: Optional[str] = None


class CategoryCreateSchema(CategorySchema):
    name: str


class CategoryUpdateSchema(CategorySchema):
    pass
