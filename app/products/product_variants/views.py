from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db.manager import get_db
from config.services import get_object_or_404
from products.product_variants.models import ProductVariant
from products.product_variants.schemas import (
    ProductVariantBaseSchema,
    ProductVariantCreateSchema,
)
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/", response_model=list[ProductVariantBaseSchema])
async def get_product_variants(db: AsyncSession = Depends(get_db)):
    return await ProductVariant.get_all(db)


@router.post("/", response_model=ProductVariantBaseSchema)
async def create_product_variant(
    body: ProductVariantCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_product_variant = ProductVariant.create(
        db,
        **body.model_dump(exclude_unset=True),
    )
    return await new_product_variant


@router.patch("/{pk}", response_model=ProductVariantBaseSchema)
async def update_product_variant(
    pk: int,
    ingredient_attrs: ProductVariantBaseSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    product_variant = await get_object_or_404(db, ProductVariant, pk)
    return await ProductVariant.update(db, product_variant, ingredient_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=ProductVariantBaseSchema)
async def delete_product_variant(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    product_variant = await get_object_or_404(db, ProductVariant, pk)
    return await ProductVariant.delete(db, product_variant)
