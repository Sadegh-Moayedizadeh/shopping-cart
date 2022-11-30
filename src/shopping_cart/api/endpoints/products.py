# View Product(done)
# View all products (see how many they are. think of something like pagination)
# Add product
# Remove product
# Show user's selected products
# Purchase the selected products

import requests
from fastapi import APIRouter, HTTPException

# from beanie import PydanticObjectId
# from starlette.responses import JSONResponse
# from fastapi import APIRouter, Depends, status
# from decimal import Decimal

# from app.Infrastructure.cart import Cart
# from app.Infrastructure.product import Product
# from app.routes import schemas
# from app.core.authentication import get_current_user, User
# from app.routes.schemas import Items

from shopping_cart.utils.products import get_single_product_api_address

router = APIRouter()


@router.get('/view-single-product/{product_id}')
def view_single_product(
    product_id: int
) -> None:
    response = requests.get(get_single_product_api_address(product_id))
    if not response.content:
        raise HTTPException(
            status_code=404,
            detail='There is no product with the given id.',
        )
    return response.json()


# @router.post('/add')
# async def add_item(add_to_cart: schemas.AddToCart, user: User = Depends(get_current_user)):
#     product = Product.get_product(add_to_cart.product_id)
#     Cart.add_to_cart(
#         user_id = user.id,
#         product_id = product[0].id,
#         product_quantity = add_to_cart.quantity
#     )
#     content = {'message': 'Add to cart.'}
#     return JSONResponse(status_code=status.HTTP_200_OK, content=content)


# @router.get('/list', response_model=schemas.Carts)
# async def carts(user: User = Depends(get_current_user)):
#     cart_items = Cart.carts(user.id)
#     product_id_list: List[PydanticObjectId] = [item.product_id for item in cart_items]
#     products = {product.id: product for product in Product.get_product(product_id_list)}
#     items = [Items(product_image = products[item.product_id].product_image,
#                    product_price = products[item.product_id].product_price,
#                    **item.__dict__)
#              for item in cart_items]
#     total_price: Decimal = sum([item.product_price for item in items])
#     return {'total_price': total_price, 'items': items}


# @router.delete('/clear')
# async def clear_cart(user: User = Depends(get_current_user)):
#     Cart.delete_all_cart_items(user.id)
#     content = {'message': 'Clear cart items.'}
#     return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=content)


# @router.delete('/delete-item-cart/{item_id}')
# async def delete_item_cart(item_id: PydanticObjectId, user: User = Depends(get_current_user)):
#     Cart.delete_cart(item_id)
#     content = {'message': 'Delete item cart.'}
#     return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=content)
