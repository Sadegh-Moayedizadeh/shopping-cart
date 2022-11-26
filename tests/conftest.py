import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from shopping_cart.models import User
from shopping_cart.settings import FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD, API_STR
from shopping_cart.main import app
from shopping_cart.crud import user_crud
from shopping_cart.schemas import UserCreate

from typing import Generator, Dict
from shopping_cart.db import SessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture
def fake_email() -> str:
    return 'fake@email.address'


@pytest.fixture
def fake_password() -> str:
    return 'p@ssword'


@pytest.fixture(scope='function')
def delete_user_by_email(db: Session, fake_email: str) -> None:
    yield
    db.query(User).filter_by(email=fake_email).delete()
    db.commit()


@pytest.fixture
def user_stub(db: Session, fake_email: str, fake_password: str, delete_user_by_email: None) -> User:
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)
    return user


@pytest.fixture
def dummy_teardown() -> None:
    print('setup')
    yield
    print('teardown')


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def superuser_token_headers(client: TestClient) -> Dict[str, str]:
#     login_data = {
#         "username": FIRST_SUPERUSER,
#         "password": FIRST_SUPERUSER_PASSWORD,
#     }
#     r = client.post(
#         f"{API_STR}/login/access-token", data=login_data)
#     tokens = r.json()
#     a_token = tokens["access_token"]
#     headers = {"Authorization": f"Bearer {a_token}"}
#     return headers
