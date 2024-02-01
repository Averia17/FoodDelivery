from fastapi import APIRouter

from products.categories.views import router as category_router
from products.ingredients.views import router as ingredient_router
from products.views import router as product_router
from users.auth.views import router as login_router
from users.views import router as user_router

api_router = APIRouter()
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(login_router, prefix="/auth", tags=["auth"])
api_router.include_router(product_router, prefix="/products", tags=["products"])
api_router.include_router(category_router, prefix="/categories", tags=["categories"])
api_router.include_router(ingredient_router, prefix="/ingredients", tags=["ingredients"])
