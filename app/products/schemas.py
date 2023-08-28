from typing import Optional

from pydantic import BaseModel


class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True
    description: Optional[str] = None
    discount: Optional[int] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductCreateSchema(ProductSchema):
    name: str
    is_active: bool = True
    discount: int = 0
    price: float
    category_id: int


class ProductUpdateSchema(ProductSchema):
    pass
