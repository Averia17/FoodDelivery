from fastapi import APIRouter
from users.views import router as user_router
from login.views import router as login_router


api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(login_router, prefix="/login", tags=["login"])
