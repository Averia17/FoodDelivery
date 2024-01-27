from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from config.db.manager import get_db
from products.ingredients.models import Ingredient
from products.models import Product


async def get_object_or_404(db, model, pk):
    obj = await model.get(db, pk)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model} with id {pk} not found")
    return obj


async def set_ingredients_to_product(
    product_id: int,
    ingredients,
    db: AsyncSession = Depends(get_db),
):
    product = await db.scalar(
        select(Product).where(Product.id == product_id).options(selectinload(Product.ingredients)),
    )
    product.ingredients = []
    for ingredient_id in ingredients:
        ingredient = await db.scalar(select(Ingredient).where(Ingredient.id == ingredient_id))
        product.ingredients.append(ingredient)
    await db.commit()
    await db.refresh(product)
