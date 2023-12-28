from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter

from pydantic import BaseModel

from products.models import Product


class ProductFilter(Filter):
    price__lte: Optional[float] = None
    price__gte: Optional[float] = None
    category_id: Optional[int] = None
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Product
        search_field_name = "search"
        search_model_fields = ["name", ]


class ProductSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True
    description: Optional[str] = None
    discount: Optional[int] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


class ProductCreateSchema(BaseModel):
    name: str
    is_active: bool = True
    discount: int = 0
    price: float
    category_id: int


class ProductUpdateSchema(ProductSchema):
    pass
