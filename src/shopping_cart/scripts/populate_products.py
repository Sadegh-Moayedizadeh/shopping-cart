import requests

from shopping_cart.crud import product_crud
from shopping_cart.schemas import ProductCreate
from shopping_cart.db import SessionLocal


def populate_products() -> None:
    all_products = requests.get('https://fakestoreapi.com/products')
    for product_dict in all_products:
        product_in = ProductCreate(**product_dict)
        product_crud.create(db=SessionLocal(), obj_in=product_in)
