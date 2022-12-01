from contextlib import suppress
from typing import Any, Dict, Optional, Union

import requests
from sqlalchemy.orm import Session

from shopping_cart.crud.base import CRUDBase
from shopping_cart.models import User
from shopping_cart.schemas import UserCreate, UserProductIds, UserUpdate
from shopping_cart.utils.products import get_single_product_api_address
from shopping_cart.utils.security import get_password_hash, verify_password


class UserCRUD(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return
        if not verify_password(password, user.hashed_password):
            return
        return user

    def add_product(self, db: Session, *, product_id: int, email: str) -> Optional[User]:
        if not requests.get(get_single_product_api_address(product_id)).content:
            return

        user = self.get_by_email(db=db, email=email)
        if not user:
            return

        current_product_ids = list(user.product_ids)
        updated_product_ids = current_product_ids + [product_id]
        update_data = UserProductIds(product_ids=updated_product_ids)
        return super().update(db, db_obj=user, obj_in=update_data)

    def remove_product(self, db: Session, *, product_id: int, email: str) -> User:
        user = self.get_by_email(db=db, email=email)
        if not user:
            return

        current_product_ids = list(user.product_ids)
        updated_product_ids = current_product_ids.copy()
        with suppress(ValueError):
            updated_product_ids.remove(product_id)
        update_data = UserProductIds(product_ids=updated_product_ids)
        return super().update(db, db_obj=user, obj_in=update_data)

    def remove_all_products(self, db: Session, *, email: str) -> User:
        user = self.get_by_email(db=db, email=email)
        if not user:
            return

        updated_product_ids = []
        update_data = UserProductIds(product_ids=updated_product_ids)
        return super().update(db, db_obj=user, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_crud = UserCRUD(User)
