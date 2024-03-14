from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel

from products.categories.schemas import CategorySchema
from products.ingredients.schemas import IngredientSchema
from products.models import Product


class ProductFilter(Filter):
    # TODO: price is option of product_variant, we need to add filter there
    # price__lte: Optional[float] = None
    # price__gte: Optional[float] = None
    category_id: Optional[int] = None
    search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Product
        search_field_name = "search"
        search_model_fields = [
            "name",
        ]


class ProductBaseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    is_active: Optional[bool] = True
    description: Optional[str] = None
    discount: Optional[int] = None


class ProductSchema(ProductBaseSchema):
    category_id: Optional[int] = None


class ProductDetailedSchema(ProductBaseSchema):
    category: Optional[CategorySchema] = None
    ingredients: Optional[list[IngredientSchema]] = None


class ProductCreateSchema(BaseModel):
    name: str
    is_active: bool = True
    discount: int = 0
    category_id: int
    ingredients: list[int]


class ProductUpdateSchema(ProductSchema):
    ingredients: Optional[list[int]] = None
