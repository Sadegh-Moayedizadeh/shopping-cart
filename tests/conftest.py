import pytest
from sqlalchemy.orm import Session
from shopping_cart.models import User

from typing import Generator
from shopping_cart.db import SessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture
def fake_email() -> str:
    return 'fake@email.address'


@pytest.fixture(scope='function')
def delete_user_by_email(db: Session, fake_email: str) -> None:
    yield
    db.query(User).filter_by(email=fake_email).delete()
    db.commit()


@pytest.fixture
def dummy_teardown() -> None:
    print('setup')
    yield
    print('teardown')
