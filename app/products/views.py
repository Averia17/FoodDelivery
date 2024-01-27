from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from config.db.manager import get_db
from config.services import get_object_or_404, set_ingredients_to_product
from products.models import Product
from products.schemas import (
    ProductCreateSchema,
    ProductDetailedSchema,
    ProductFilter,
    ProductSchema,
    ProductUpdateSchema,
)
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/{pk}", response_model=ProductDetailedSchema)
async def get_product(pk: int, db: AsyncSession = Depends(get_db)):
    product = await db.scalar(
        select(Product)
        .where(Product.id == pk)
        .options(joinedload(Product.category))
        .options(selectinload(Product.ingredients))
    )
    return product


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    product_filter: ProductFilter = FilterDepends(ProductFilter), db: AsyncSession = Depends(get_db)
):
    query = product_filter.filter(select(Product))
    products = await Product.filter(db, query)
    return products


@router.post("/", response_model=ProductSchema)
async def create_product(
    body: ProductCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    body = body.model_dump(exclude_unset=True)
    ingredients = body.pop("ingredients")

    new_product = await Product.create(
        db,
        **body,
    )
    await set_ingredients_to_product(new_product.id, ingredients, db)
    return new_product


@router.patch("/{pk}", response_model=ProductSchema)
async def update_product(
    pk: int,
    product_attrs: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    product_attrs = product_attrs.model_dump(exclude_unset=True)
    product = await get_object_or_404(db, Product, pk)
    try:
        ingredients = product_attrs.pop("ingredients")
    except KeyError:
        return await Product.update(db, product, product_attrs)

    # TODO: Тут ингредиенты польностью перезаписываются, при изменении ингредиентов в продукте, нужно заново прописывать
    #  весь список, нужно подумать подходит ли нам такой вариант, или нужно переделать.

    await set_ingredients_to_product(pk, ingredients, db)

    return await Product.update(db, product, product_attrs)


@router.delete("/{pk}", response_model=ProductSchema)
async def delete_product(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    product = await get_object_or_404(db, Product, pk)
    return await Product.delete(db, product)
