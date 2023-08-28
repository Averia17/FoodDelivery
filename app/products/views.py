from pydantic import BaseModel
from sqlalchemy import select

from config.db.manager import get_db, is_current_user_manager
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from products.models import Product as ProductModel
from products.schemas import ProductSchema, ProductCreateSchema, ProductUpdateSchema
from products.services import filtering

router = APIRouter()


@router.get("/{pk}", response_model=ProductSchema)
async def get_product(pk: int, db: AsyncSession = Depends(get_db)):
    return await ProductModel.get(db, pk)


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    db: AsyncSession = Depends(get_db),
    category_id: int | None = None,
    price__gte: float | None = None,
    price__lte: float | None = None,
):
    params = locals().copy()

    valid_params = dict()
    list_of_valid_params = list(ProductSchema.model_fields)

    for param in params:
        param_as_field_name = param.split("__")[0]
        if params[param] and param_as_field_name in list_of_valid_params:
            valid_params[param] = params[param]

    products = await ProductModel.get_all(db)
    products = filtering(products, valid_params)
    return products


@router.post("/", response_model=ProductSchema)
async def create_product(
    body: ProductCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_product = ProductModel.create(
        db,
        name=body.name,
        is_active=body.is_active,
        description=body.description,
        discount=body.discount,
        price=body.price,
        category_id=body.category_id,
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
