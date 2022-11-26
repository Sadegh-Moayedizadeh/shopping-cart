from fastapi import APIRouter

from shopping_cart.api.endpoints import login, user

api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
api_router.include_router(user.router, prefix='/users', tags=['users'])
