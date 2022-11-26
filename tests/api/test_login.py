from typing import Dict

from fastapi.testclient import TestClient

from shopping_cart.models import User
from shopping_cart.settings import (API_STR, FIRST_SUPERUSER,
                                    FIRST_SUPERUSER_PASSWORD)


def test_get_access_token(
    client: TestClient,
    user_stub: User,
    fake_email:str,
    fake_password: str
) -> None:
    # Arrange
    login_data = {
        'username': fake_email,
        'password': fake_password,
    }

    # Act
    response = client.post('{}/login/access-token'.format(API_STR), data=login_data)
    tokens = response.json()

    # Assert
    assert response.status_code == 200
    assert 'access_token' in tokens
    assert tokens['access_token']


def test_use_access_token(
    client: TestClient, user_stub_token_headers: Dict[str, str]
) -> None:
    # Arrange, Act
    response = client.post(
        '{}/login/test-token'.format(API_STR),
        headers=user_stub_token_headers
    )
    result = response.json()

    # Assert
    assert response.status_code == 200
    assert 'email' in result
