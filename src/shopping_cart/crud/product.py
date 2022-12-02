from typing import List

from sqlalchemy.orm import Session

from shopping_cart.crud.base import CRUDBase
from shopping_cart.models import Product
from shopping_cart.schemas import ProductCreate, ProductUpdate


class ProductCRUD(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_multi_by_cart(
        self, db: Session, *, cart_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(self.model)
            .filter(Product.cart_id == cart_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


product_crud = ProductCRUD(Product)
