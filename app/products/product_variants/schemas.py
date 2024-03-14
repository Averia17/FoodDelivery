from typing import Annotated, Optional

from fastapi.params import Path
from pydantic import BaseModel


class ProductVariantBaseSchema(BaseModel):
    id: Optional[int] = None
    product_id: Optional[int] = None
    price: Optional[Annotated[int, Path(gt=0)]] = None
    discount: Optional[Annotated[int, Path(ge=0, lt=100)]] = 0
    weight: Optional[int] = None


class ProductVariantCreateSchema(BaseModel):
    product_id: int
    price: Annotated[int, Path(gt=0)]
    discount: Optional[Annotated[int, Path(ge=0, lt=100)]] = 0
    weight: int
