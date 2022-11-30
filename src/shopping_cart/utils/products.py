def get_single_product_api_address(product_id: int) -> str:
    return 'https://fakestoreapi.com/products/' + str(product_id)


def get_all_products_api_address() -> str:
    return 'https://fakestoreapi.com/products'
