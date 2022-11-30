from fastapi.testclient import TestClient
from shopping_cart.settings import API_STR


def test_view_product_with_non_existing_id_should_return_404_response(
    client: TestClient
) -> None:
    # Arrange, Act
    response = client.get(
        '{}/products/view-single-product/{}'.format(API_STR, '-1')
    )
    # Assert
    assert response.status_code == 404


def test_view_product_with_an_existing_id_should_return_200_response(
    client: TestClient
) -> None:
    # Arrange, Act
    response = client.get(
        '{}/products/view-single-product/{}'.format(API_STR, '1')
    )
    # Assert
    assert response.status_code == 200


def test_view_all_products_should_always_return_200_response(
    client: TestClient
) -> None:
    # Arrange, Act
    response = client.get(
        '{}/products/view-all-products'.format(API_STR)
    )
    # Assert
    assert response.status_code == 200


def test_add_product_should_update_users_product_ids() -> None:
    pass


def test_add_product_id_that_does_not_exist_should_raise_error() -> None:
    pass


def test_remove_product_should_remove_its_id_from_users_product_ids() -> None:
    pass


def test_remove_product_that_is_not_present_in_users_product_ids_should_raise_error() -> None:  # noqa: E501
    pass


def test_show_users_selected_products_should_return_all_its_product_ids() -> None:  # noqa: E501
    pass


def test_purchase_selected_products_should_empty_users_product_ids() -> None:
    pass
