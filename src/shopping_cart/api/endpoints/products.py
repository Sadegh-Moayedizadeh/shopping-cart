from typing import Any

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shopping_cart import schemas
from shopping_cart.crud import user_crud, product_crud
from shopping_cart.models import User
from shopping_cart.utils.db import get_db
from shopping_cart.utils.products import (get_all_products_api_address,
                                          get_single_product_api_address)
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
def veiw_all_products() -> Any:
    return requests.get(get_all_products_api_address()).json()


@router.put('/add-product', response_model=schemas.User)
def add_product_to_user(
    *,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    user = user_crud.add_product(
        db=db,
        product_id=product_id,
        email=current_user.email
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail='No product with the given id or no user.',
        )
    return user


@router.put('/remove-product', response_model=schemas.User)
def remove_product_from_user(
    *,
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    user = user_crud.remove_product(
        db=db,
        product_id=product_id,
        email=current_user.email
    )
    if not user:
        raise HTTPException(
            status_code=404,
            detail='No product with the given id or no user.',
        )
    return user


@router.get('/all-selected-products')
def get_all_products_for_user(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return current_user.product_ids


@router.put('/purchase', response_model=schemas.User)
def purchase(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    return user_crud.remove_all_products(db=db, email=current_user.email)
