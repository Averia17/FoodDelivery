from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db.manager import get_db
from users.auth.schemas import Token
from users.auth.services import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from users.models import User

router = APIRouter()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | Exception:
    user = await User.get_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(user_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, user_data.username, user_data.password)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}
