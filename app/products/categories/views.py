from config.db.manager import get_db, is_current_user_manager
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from products.categories.models import Category as CategoryModel
from products.categories.schemas import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema

router = APIRouter()


@router.get("/{pk}", response_model=CategorySchema)
async def get_category(pk: int, db: AsyncSession = Depends(get_db)):
    return await CategoryModel.get(db, pk)


@router.get("/", response_model=list[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryModel.get_all(db)


@router.post("/", response_model=CategorySchema)
async def create_category(
    body: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
    # is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_category = CategoryModel.create(
        db,
        name=body.name,
    )
    return await new_category


@router.patch("/{pk}", response_model=CategorySchema)
async def update_category(
    pk: int,
    category_attrs: CategoryUpdateSchema,
    db: AsyncSession = Depends(get_db),
    # is_manager: Exception | None = Depends(is_current_user_manager),
):
    return await CategoryModel.update(db, pk, category_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=CategorySchema)
async def delete_category(
    pk: int, db: AsyncSession = Depends(get_db),
    # is_manager: Exception | None = Depends(is_current_user_manager)
):
    category = await CategoryModel.get(db, pk)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await CategoryModel.delete(db, pk)
    return category
