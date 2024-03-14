from typing import Annotated, Optional

from fastapi.params import Path
from pydantic import BaseModel

from products.product_variants.schemas import ProductVariantBaseSchema
from users.schemas import UserSchema


class BasketProductBaseSchema(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    product_variant_id: Optional[int] = None
    count: Optional[int] = None


class BasketProductDetailedSchema(BasketProductBaseSchema):
    user: Optional[UserSchema] = None
    product_variant: Optional[ProductVariantBaseSchema] = None


class BasketSchema(BaseModel):
    basket_products: Optional[list[BasketProductDetailedSchema]] = None
    basket_price: Optional[int] = None


class BasketProductCreateSchema(BaseModel):
    product_variant_id: int
    count: Annotated[int, Path(ge=1)]


class BasketProductUpdateSchema(BaseModel):
    count: Annotated[int, Path(ge=1)]
