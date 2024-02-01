from typing import Optional

from pydantic import BaseModel


class IngredientSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class IngredientCreateSchema(IngredientSchema):
    name: str
