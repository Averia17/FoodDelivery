from config.db.manager import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User as UserModel
from users.schemas import UserSchema, UserUpdateSchema

router = APIRouter()


@router.get("/{pk}", response_model=UserSchema)
async def get_user(pk: int, db: AsyncSession = Depends(get_db)):
    return await UserModel.get(db, pk)


@router.get("/", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserModel.get_all(db)


@router.post("/", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    return await UserModel.create(db, **user.model_dump())


@router.patch("/{pk}", response_model=UserSchema)
async def update_user(pk: int, user_attrs: UserUpdateSchema, db: AsyncSession = Depends(get_db)):
    return await UserModel.update(db, pk, user_attrs.model_dump(exclude_unset=True))
