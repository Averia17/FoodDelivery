from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from config.db.manager import get_db, get_current_user_from_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from users.auth.services import verify_password, create_access_token, create_refresh_token
from users.auth.schemas import Token
from users.models import User as UserModel

router = APIRouter()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await UserModel.get_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token}
