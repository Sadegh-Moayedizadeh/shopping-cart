from sqlalchemy.orm import Session

from shopping_cart.crud.base import CRUDBase
from shopping_cart.models import Cart, Product
from shopping_cart.schemas import CartCreate, CartUpdate


class CartCRUD(CRUDBase[Cart, CartCreate, CartUpdate]):
    def update_with_product(
        self,
        db: Session,
        *,
        db_obj: Cart,
        product: Product
    ) -> Cart:
        db_obj.products.append(product)
        db.commit()
        return db_obj


cart_crud = CartCRUD(Cart)
