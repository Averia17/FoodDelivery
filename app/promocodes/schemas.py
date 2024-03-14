import datetime
from typing import Annotated, Optional

from fastapi.params import Path
from pydantic import BaseModel

from products.product_variants.schemas import ProductVariantBaseSchema


class PromoCodeBaseSchema(BaseModel):
    id: Optional[str] = None
    valid_from: Optional[datetime.datetime] = None
    valid_until: Optional[datetime.datetime] = None
    discount: Optional[Annotated[int, Path(ge=1, lt=100)]] = None
    description: Optional[str] = None


class PromoCodeDetailedSchema(PromoCodeBaseSchema):
    product_variants: Optional[list[ProductVariantBaseSchema]] = []


class PromoCodeCreateSchema(PromoCodeBaseSchema):
    id: str
    valid_from: Optional[datetime.datetime] = datetime.datetime.now(datetime.UTC)
    valid_until: datetime.datetime
    product_variants: Optional[list[int]] = []


class PromoCodeUpdateSchema(BaseModel):
    valid_from: Optional[datetime.datetime] = None
    valid_until: Optional[datetime.datetime] = None
    discount: Optional[Annotated[int, Path(ge=1, lt=100)]] = None
    description: Optional[str] = None
    product_variants: Optional[list[int]] = None
