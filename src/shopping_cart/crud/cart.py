from shopping_cart.crud.base import CRUDBase
from shopping_cart.models import Cart
from shopping_cart.schemas import CartCreate, CartUpdate


class CartCRUD(CRUDBase[Cart, CartCreate, CartUpdate]):
    pass


cart_crud = CartCRUD(Cart)
