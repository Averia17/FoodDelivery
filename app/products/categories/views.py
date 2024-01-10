from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db.manager import get_db
from config.services import get_object_or_404
from products.categories.models import Category
from products.categories.schemas import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/{pk}", response_model=CategorySchema)
async def get_category(pk: int, db: AsyncSession = Depends(get_db)):
    return await get_object_or_404(db, Category, pk)


@router.get("/", response_model=list[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await Category.get_all(db)


@router.post("/", response_model=CategorySchema)
async def create_category(
    body: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_category = Category.create(
        db,
        name=body.name,
    )
    return await new_category


@router.patch("/{pk}", response_model=CategorySchema)
async def update_category(
    pk: int,
    category_attrs: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    category = await get_object_or_404(db, Category, pk)
    return await Category.update(db, category, category_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=CategorySchema)
async def delete_category(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    category = await get_object_or_404(db, Category, pk)
    return await Category.delete(db, category)
