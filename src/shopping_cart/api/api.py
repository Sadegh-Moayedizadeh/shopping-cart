from fastapi import APIRouter
from shopping_cart.api.endpoints import user, login


api_router = APIRouter()

api_router.include_router(login.router, tags=['login'])
