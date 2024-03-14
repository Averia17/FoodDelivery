import datetime

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from config.db.manager import get_db
from products.ingredients.models import Ingredient
from products.models import Product
from products.product_variants.models import ProductVariant
from promocodes.models import PromoCode


async def get_object_or_404(db, model, pk):
    obj = await model.get(db, pk)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{model} with id {pk} not found")
    return obj


# TODO: I think we need to combine "set_ingredients_to_product" and "set_product_variants_to_promo_code".
#  But we need to give Models_name as argument of function. I dont know what way is better
async def set_ingredients_to_product(
    product_id: int,
    ingredients: list[int],
    db: AsyncSession = Depends(get_db),
):
    product = await db.scalar(
        select(Product).where(Product.id == product_id).options(selectinload(Product.ingredients)),
    )
    ingredients = await db.scalars(select(Ingredient).where(Ingredient.id.in_(ingredients)))
    product.ingredients = list(ingredients)
    await db.commit()
    await db.refresh(product)


async def set_product_variants_to_promo_code(
    promo_code_id: str,
    product_variants: list[int],
    db: AsyncSession = Depends(get_db),
):
    promo_code = await db.scalar(
        select(PromoCode).where(PromoCode.id == promo_code_id).options(selectinload(PromoCode.product_variants)),
    )
    product_variants = await db.scalars(select(ProductVariant).where(ProductVariant.id.in_(product_variants)))
    promo_code.product_variants = list(product_variants)
    await db.commit()
    await db.refresh(promo_code)


def validate_datetimes(valid_from: datetime.datetime, valid_until: datetime.datetime):
    if valid_until <= valid_from:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"valid_from({valid_from}) should be less than valid_until({valid_until})",
        )
