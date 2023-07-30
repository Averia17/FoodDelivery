from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from starlette import status

from config import settings
from config.db.manager import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.security import verify_password, create_access_token
from login.schemas import Token
from users.models import User as UserModel

router = APIRouter()


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = (await db.execute(select(UserModel).where(UserModel.email == email))).scalars().first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
