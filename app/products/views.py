from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db.manager import get_db
from config.services import get_object_or_404
from products.models import Product
from products.schemas import (
    ProductCreateSchema,
    ProductFilter,
    ProductSchema,
    ProductUpdateSchema,
)
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/{pk}", response_model=ProductSchema)
async def get_product(pk: int, db: AsyncSession = Depends(get_db)):
    return await get_object_or_404(db, Product, pk)


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
    new_product = Product.create(
        db,
        **body.model_dump(exclude_unset=True),
    )
    return await new_product


@router.patch("/{pk}", response_model=ProductSchema)
async def update_product(
    pk: int,
    product_attrs: ProductUpdateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    product = await get_object_or_404(db, Product, pk)
    return await Product.update(db, product, product_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=ProductSchema)
async def delete_product(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    product = await get_object_or_404(db, Product, pk)
    return await Product.delete(db, product)
