from fastapi_filter import FilterDepends

from config.db.manager import get_db, is_current_user_manager
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from products.models import Product as ProductModel
from products.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema, ProductFilter

router = APIRouter()


@router.get("/{pk}", response_model=ProductSchema)
async def get_product(pk: int, db: AsyncSession = Depends(get_db)):
    return await ProductModel.get(db, pk)


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    product_filter: ProductFilter = FilterDepends(ProductFilter),
    db: AsyncSession = Depends(get_db)
):
    query = product_filter.filter(select(ProductModel))
    products = await ProductModel.filter(db, query)
    return products


@router.post("/", response_model=ProductSchema)
async def create_product(
    body: ProductCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_product = ProductModel.create(
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
    return await ProductModel.update(db, pk, product_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=ProductSchema)
async def delete_product(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    product = await ProductModel.get(db, pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await ProductModel.delete(db, pk)
    return product
