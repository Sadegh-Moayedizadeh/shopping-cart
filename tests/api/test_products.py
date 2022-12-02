from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from shopping_cart.crud import user_crud, product_crud
from shopping_cart.schemas import ProductCreate
from shopping_cart.models import User
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
    client: TestClient,
    db: Session,
    delete_products: None
) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )
    product = product_crud.create(db=db, obj_in=product_in)

    # Act
    response = client.get(
        '{}/products/view-single-product/{}'.format(API_STR, '1')
    )
    # Assert
    assert response.status_code == 200


def test_view_all_products(
    client: TestClient,
    db: Session,
    delete_products: None
) -> None:
    # Arrange
    first_product_in = ProductCreate(
        title='first_fake_title',
        price=0,
        category='first_fake_category',
        description='first_fake_description',
        image='first_fake_image_address'
    )
    first_product = product_crud.create(db=db, obj_in=first_product_in)

    second_product_in = ProductCreate(
        title='second_fake_title',
        price=0,
        category='second_fake_category',
        description='second_fake_description',
        image='second_fake_image_address'
    )
    second_product = product_crud.create(db=db, obj_in=second_product_in)

    # Act
    response = client.get(
        '{}/products/view-all-products'.format(API_STR)
    )

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_add_product_to_user(
    client: TestClient,
    db: Session,
    user_stub: User,
    user_stub_token_headers: Dict[str, str],
    delete_users: None,
    delete_carts: None,
    delete_products: None
) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )
    product = product_crud.create(db=db, obj_in=product_in)

    # Act
    response = client.put(
        '{}/products/add-product'.format(API_STR),
        params={'product_id': product.id},
        headers=user_stub_token_headers
    )

    # Assert
    assert response.status_code == 200
    assert user_stub.cart
    assert user_stub.cart.products == [product]


def test_remove_product_from_user(
    client: TestClient,
    db: Session,
    user_stub: User,
    user_stub_token_headers: Dict[str, str],
    delete_users: None,
    delete_carts: None,
    delete_products: None
) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )
    product = product_crud.create(db=db, obj_in=product_in)

    client.put(
        '{}/products/add-product'.format(API_STR),
        params={'product_id': product.id},
        headers=user_stub_token_headers
    )

    # Assume
    assert user_stub.cart
    assert user_stub.cart.products == [product]

    # Act
    response = client.put(
        '{}/products/remove-product'.format(API_STR),
        params={'product_id': product.id},
        headers=user_stub_token_headers
    )
    db.refresh(user_stub)

    # Assert
    assert response.status_code == 200
    assert user_stub.cart.products == []


def test_show_users_selected_products_should_return_all_its_product_ids(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    user_stub: User,
    delete_users: None
) -> None:
    # Arrange
    user_crud.add_product(db=db, product_id=1, email=user_stub.email)
    db.refresh(user_stub)

    # Assume
    assert user_stub.product_ids == [1]

    # Act
    response = client.get(
        '{}/products/all-selected-products'.format(API_STR),
        headers=user_stub_token_headers
    )

    # Assert
    assert response.json() == [1]


def test_purchase_selected_products_should_empty_users_product_ids(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    user_stub: User,
    delete_users: None
) -> None:
    # Arrange
    user_crud.add_product(db=db, product_id=1, email=user_stub.email)
    user_crud.add_product(db=db, product_id=2, email=user_stub.email)
    db.refresh(user_stub)

    # Assume
    assert user_stub.product_ids == [1, 2]

    # Act
    response = client.put(
        '{}/products/purchase'.format(API_STR),
        headers=user_stub_token_headers
    )
    db.refresh(user_stub)

    # Assert
    assert response.json()['product_ids'] == []
    assert user_stub.product_ids == []
