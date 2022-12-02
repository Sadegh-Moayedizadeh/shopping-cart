from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shopping_cart import schemas
from shopping_cart.crud import user_crud
from shopping_cart.models import User
from shopping_cart.utils.db import get_db
from shopping_cart.utils.user import get_current_active_user

router = APIRouter()


@router.get('/', response_model=List[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post('/', response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail='The user with this username already exists.',
        )
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.get('/me', response_model=schemas.User)
def read_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return current_user


@router.get('/{user_id}', response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    user = user_crud.get(db, id=user_id)
    return user


@router.put('/{user_id}', response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='The user with this username does not exist.',
        )
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user
