from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db.manager import get_db
from config.services import (
    get_object_or_404,
    set_product_variants_to_promo_code,
    validate_datetimes,
)
from promocodes.models import PromoCode
from promocodes.schemas import (
    PromoCodeBaseSchema,
    PromoCodeCreateSchema,
    PromoCodeDetailedSchema,
    PromoCodeUpdateSchema,
)
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/{pk}", response_model=PromoCodeDetailedSchema)
async def get_promo_code(
    pk: str,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    promo_code = await PromoCode.get_by_promo_code_id(db=db, promo_code_id=pk)
    if not promo_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"PromoCode with id {pk} not found")
    return promo_code


@router.get("/", response_model=list[PromoCodeBaseSchema])
async def get_promo_codes(
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    return await PromoCode.get_all(db)


@router.post("/", response_model=PromoCodeBaseSchema)
async def create_promo_code(
    body: PromoCodeCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    validate_datetimes(body.valid_from, body.valid_until)

    body = body.model_dump(exclude_unset=True)
    product_variants = body.pop("product_variants", [])

    new_promo_code = await PromoCode.create(
        db,
        **body,
    )
    await set_product_variants_to_promo_code(new_promo_code.id, product_variants, db)
    return new_promo_code


@router.patch("/{pk}", response_model=PromoCodeBaseSchema)
async def update_promo_code(
    pk: str,
    promo_code_attrs: PromoCodeUpdateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    promo_code = await get_object_or_404(db, PromoCode, pk)
    body = promo_code_attrs.model_dump(exclude_unset=True)

    valid_from = body.get("valid_from", promo_code.valid_from)
    valid_until = body.get("valid_until", promo_code.valid_until)
    validate_datetimes(valid_from, valid_until)

    product_variants = body.pop("product_variants", [])
    if product_variants:
        await set_product_variants_to_promo_code(pk, product_variants, db)
    return await PromoCode.update(db, promo_code, body)


@router.delete("/{pk}", response_model=PromoCodeBaseSchema)
async def delete_promo_code(
    pk: str, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    promo_code = await get_object_or_404(db, PromoCode, pk)
    return await PromoCode.delete(db, promo_code)
