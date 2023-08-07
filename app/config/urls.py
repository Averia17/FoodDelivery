from fastapi import APIRouter
from users.views import router as user_router
from users.auth.views import router as login_router


api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(login_router, prefix="/auth", tags=["auth"])
