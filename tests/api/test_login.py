from typing import Dict

from fastapi.testclient import TestClient

from shopping_cart.settings import FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD, API_STR
from shopping_cart.models import User

# from app.core.config import settings


def test_get_access_token(
    client: TestClient,
    user_stub: User,
    fake_email:str,
    fake_password: str
) -> None:
    login_data = {
        "username": fake_email,
        "password": fake_password,
    }
    r = client.post(f"{API_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


# def test_use_access_token(
#     client: TestClient, superuser_token_headers: Dict[str, str]
# ) -> None:
#     r = client.post(
#         f"{settings.API_V1_STR}/login/test-token", headers=superuser_token_headers,
#     )
#     result = r.json()
#     assert r.status_code == 200
#     assert "email" in result
