from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db.manager import get_db
from config.services import get_object_or_404
from products.ingredients.models import Ingredient
from products.ingredients.schemas import IngredientCreateSchema, IngredientSchema
from users.auth.services import is_current_user_manager

router = APIRouter()


@router.get("/{pk}", response_model=IngredientSchema)
async def get_ingredient(pk: int, db: AsyncSession = Depends(get_db)):
    return await get_object_or_404(db, Ingredient, pk)


@router.get("/", response_model=list[IngredientSchema])
async def get_ingredients(db: AsyncSession = Depends(get_db)):
    return await Ingredient.get_all(db)


@router.post("/", response_model=IngredientSchema)
async def create_ingredient(
    body: IngredientCreateSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    new_ingredient = Ingredient.create(
        db,
        name=body.name,
    )
    return await new_ingredient


@router.patch("/{pk}", response_model=IngredientSchema)
async def update_ingredient(
    pk: int,
    ingredient_attrs: IngredientSchema,
    db: AsyncSession = Depends(get_db),
    is_manager: Exception | None = Depends(is_current_user_manager),
):
    ingredient = await get_object_or_404(db, Ingredient, pk)
    return await Ingredient.update(db, ingredient, ingredient_attrs.model_dump(exclude_unset=True))


@router.delete("/{pk}", response_model=IngredientSchema)
async def delete_ingredient(
    pk: int, db: AsyncSession = Depends(get_db), is_manager: Exception | None = Depends(is_current_user_manager)
):
    ingredient = await get_object_or_404(db, Ingredient, pk)
    return await Ingredient.delete(db, ingredient)
