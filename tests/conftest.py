import pytest

from typing import Generator
from shopping_cart.db import SessionLocal


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()
