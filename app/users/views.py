from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db.manager import get_db
from config.services import get_object_or_404
from users.auth.services import get_password_hash
from users.models import User
from users.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

router = APIRouter()


@router.get("/{pk}", response_model=UserSchema)
async def get_user(pk: int, db: AsyncSession = Depends(get_db)):
    return await get_object_or_404(db, User, pk)


@router.get("/", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await User.get_all(db)


@router.post("/", response_model=UserSchema)
async def create_user(body: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    new_user = User.create(
        db,
        email=body.email,
        phone_number=body.phone_number,
        password=get_password_hash(body.password),
    )
    return await new_user


@router.patch("/{pk}", response_model=UserSchema)
async def update_user(pk: int, user_attrs: UserUpdateSchema, db: AsyncSession = Depends(get_db)):
    user = await get_object_or_404(db, User, pk)
    return await User.update(db, user, user_attrs.model_dump(exclude_unset=True))
