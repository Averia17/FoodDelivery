from fastapi import APIRouter

from users.schemas import User
from users.views import get_user

api_router = APIRouter()
api_router.add_api_route("/", get_user, methods=["GET"], response_model=User)
