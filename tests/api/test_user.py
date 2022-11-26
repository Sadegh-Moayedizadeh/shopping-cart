from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from shopping_cart.crud import user_crud
from shopping_cart.models import User
from shopping_cart.schemas import UserCreate
from shopping_cart.settings import API_STR


def test_get_users(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    fake_email: str
) -> None:
    # Arrange, Act
    response = client.get(
        '{}/users/me'.format(API_STR),
        headers=user_stub_token_headers
    )
    current_user = response.json()

    # Assert
    assert response.status_code == 200
    assert current_user
    assert current_user['is_active'] is True
    assert current_user['is_superuser'] is False
    assert current_user['email'] == fake_email


def test_create_new_user(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    delete_users: None
) -> None:
    # Arrange
    email_address = 'another.fake@email.address'
    data = {'email': 'another.fake@email.address', 'password': 'p@ssword'}

    # Act
    response = client.post(
        '{}/users/'.format(API_STR),
        headers=user_stub_token_headers,
        json=data
    )
    created_user = response.json()
    user = user_crud.get_by_email(db, email=email_address)

    # Assert
    assert response.status_code == 200
    assert user
    assert user.email == created_user['email']


def test_get_an_existing_user_by_id(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    delete_users: None
) -> None:
    # Arrange
    email = 'another.fake@email.address'
    user_in = UserCreate(email=email, password='p@ssword')
    user_id = user_crud.create(db, obj_in=user_in).id

    # Act
    response = client.get(
        '{}/users/{}'.format(API_STR, user_id),
        headers=user_stub_token_headers,
    )
    api_user = response.json()
    existing_user = user_crud.get_by_email(db, email=email)

    # Assert
    assert response.status_code == 200
    assert existing_user
    assert existing_user.email == api_user['email']


def test_create_user_with_existing_username(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    user_stub: User,
    fake_email: str,
    fake_password: str
) -> None:
    # Arrange
    data = {'email': fake_email, 'password': fake_password}

    # Act
    response = client.post(
        '{}/users/'.format(API_STR),
        headers=user_stub_token_headers,
        json=data
    )

    # Assert
    assert response.status_code == 400
