from typing import Any

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shopping_cart import schemas
from shopping_cart.crud import user_crud, product_crud, cart_crud
from shopping_cart.models import User
from shopping_cart.utils.db import get_db
from shopping_cart.utils.user import get_current_active_user

router = APIRouter()


@router.get('/view-single-product/{product_id}')
def view_single_product(
    product_id: int,
    db=Depends(get_db)
) -> Any:
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail='There is no product with the given id.',
        )
    return product


@router.get('/view-all-products')
def view_all_products(db=Depends(get_db)) -> Any:
    return product_crud.get_multi(db=db)


@router.put('/add-product', response_model=schemas.User)
def add_product_to_user(
    *,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    product = product_crud.get(db=db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail='There is no product with the given id.',
        )

    cart = current_user.cart
    if not cart:
        cart_in = schemas.CartCreate()
        new_cart = cart_crud.create(db=db, obj_in=cart_in)
        user_crud.update_with_cart(db=db, cart=new_cart, db_obj=current_user)
        cart = new_cart

    return cart_crud.update_with_product(db=db, db_obj=cart, product=product)


@router.put('/remove-product', response_model=schemas.User)
def remove_product_from_user(
    *,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return product_crud.remove(db=db, id=product_id)


@router.get('/all-selected-products')
def get_all_products_for_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return current_user.cart.products
