from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from shopping_cart.settings import API_STR
from shopping_cart.schemas import UserCreate
from shopping_cart.crud import user_crud
from shopping_cart.models import User


def test_get_users(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    fake_email: str
) -> None:
    r = client.get(f"{API_STR}/users/me", headers=user_stub_token_headers)
    current_user = r.json()
    assert r.status_code == 200
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == fake_email


def test_create_new_user(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    delete_users: None
) -> None:
    email_address = 'another.fake@email.address'
    data = {"email": "another.fake@email.address", "password": 'p@ssword'}
    r = client.post(
        f"{API_STR}/users/", headers=user_stub_token_headers, json=data
    )
    created_user = r.json()
    user = user_crud.get_by_email(db, email=email_address)
    assert r.status_code == 200
    assert user
    assert user.email == created_user["email"]


def test_get_an_existing_user_by_id(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    delete_users: None
) -> None:
    email = 'another.fake@email.address'
    user_in = UserCreate(email=email, password='p@ssword')
    user = user_crud.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{API_STR}/users/{user_id}", headers=user_stub_token_headers,
    )
    api_user = r.json()
    existing_user = user_crud.get_by_email(db, email=email)
    assert r.status_code == 200
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_with_existing_username(
    client: TestClient,
    user_stub_token_headers: Dict[str, str],
    db: Session,
    user_stub: User,
    fake_email: str,
    fake_password: str
) -> None:
    data = {"email": fake_email, "password": fake_password}
    r = client.post(
        f"{API_STR}/users/", headers=user_stub_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_update_user() -> None:
    pass
