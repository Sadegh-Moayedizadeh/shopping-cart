from typing import Dict
from sqlalchemy.orm import Session

from fastapi.testclient import TestClient

from shopping_cart.settings import API_STR
from shopping_cart.models import User
from shopping_cart.crud import user_crud


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


def test_add_product_should_update_users_product_ids(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    user_stub: User,
    delete_users: None
) -> None:
    # Arrange
    response = client.put(
        '{}/products/add-product'.format(API_STR),
        params={'product_id': 1},
        headers=user_stub_token_headers
    )

    # Act
    updated_user_json = response.json()
    db.refresh(user_stub)

    # Assert
    assert response.status_code == 200
    assert updated_user_json['product_ids'] == [1]
    assert user_stub.product_ids == [1]


def test_add_product_with_non_existing_id_should_return_404_response(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    user_stub: User,
    db: Session,
    delete_users: None
) -> None:
    # Arrange, Act
    response = client.put(
        '{}/products/add-product'.format(API_STR),
        params={'product_id': -1},
        headers=user_stub_token_headers
    )
    db.refresh(user_stub)

    # Assert
    assert response.status_code == 404
    assert user_stub.product_ids == []


def test_add_product_for_an_unauthorized_user_should_return_401_response(
    client: TestClient,
    user_stub: User,
    db: Session,
    delete_users: None
) -> None:
    # Arrange, Act
    response = client.put(
        '{}/products/add-product'.format(API_STR),
        params={'product_id': 1}
    )
    db.refresh(user_stub)

    # Assert
    assert response.status_code == 401
    assert user_stub.product_ids == []


def test_remove_product_should_remove_its_id_from_users_product_ids() -> None:
    pass


def test_remove_product_that_is_not_present_in_users_product_ids_should_raise_error() -> None:  # noqa: E501
    pass


def test_show_users_selected_products_should_return_all_its_product_ids() -> None:  # noqa: E501
    pass


def test_purchase_selected_products_should_empty_users_product_ids() -> None:
    pass
