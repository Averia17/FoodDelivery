import math

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from basket.models import BasketProduct
from basket.schemas import (
    BasketProductBaseSchema,
    BasketProductCreateSchema,
    BasketProductUpdateSchema,
    BasketSchema,
)
from config.db.manager import get_db
from config.services import get_object_or_404
from users.auth.services import get_current_user_from_token, is_current_user_owner
from users.models import User

router = APIRouter()


@router.get("/", response_model=BasketSchema)
async def get_all_basket_products_of_current_user(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    basket_products = await BasketProduct.get_by_user_id(db=db, user_id=user.id)
    basket_price = 0

    basket_products = basket_products.all()
    for prod in basket_products:
        basket_price += math.ceil(
            (prod.product_variant.price * (100 - prod.product_variant.discount) / 100) * prod.count
        )

    return {"basket_products": basket_products, "basket_price": basket_price}


@router.post("/add_product/", response_model=BasketProductBaseSchema)
async def create_basket_product(
    body: BasketProductCreateSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    body = body.model_dump(exclude_unset=True)
    new_basket_product = await BasketProduct.create(
        db,
        user_id=user.id,
        **body,
    )
    return new_basket_product


@router.patch("/update_product/{pk}", response_model=BasketProductBaseSchema)
async def update_basket_product(
    pk: int,
    basket_product_attrs: BasketProductUpdateSchema,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    basket_product_attrs = basket_product_attrs.model_dump(exclude_unset=True)
    basket_product = await get_object_or_404(db, BasketProduct, pk)
    await is_current_user_owner(basket_product.user_id, user)
    return await BasketProduct.update(db, basket_product, basket_product_attrs)


@router.delete("/delete_product/{pk}", response_model=BasketProductBaseSchema)
async def delete_basket_product(
    pk: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_from_token),
):
    basket_product = await get_object_or_404(db, BasketProduct, pk)
    await is_current_user_owner(basket_product.user_id, user)
    return await BasketProduct.delete(db, basket_product)
