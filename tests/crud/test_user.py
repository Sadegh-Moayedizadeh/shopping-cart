from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from shopping_cart.crud import user_crud
from shopping_cart.utils.security import verify_password
from shopping_cart.schemas import UserCreate, UserUpdate
from shopping_cart.models import User


def test_create_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange, Act
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)

    # Assert
    assert user.email == fake_email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)

    # Act
    authenticated_user = user_crud.authenticate(
        db, email=fake_email, password=fake_password)

    # Assert
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_non_existing_user_should_not_authenticate(
    db: Session,
    fake_email: str,
    fake_password: str
) -> None:
    # Arrange, Act
    user = user_crud.authenticate(
        db, email=fake_email, password=fake_password)

    # Assert
    assert user is None


def test_created_user_should_be_active(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)

    # Act
    is_active = user_crud.is_active(user)

    # Assert
    assert is_active is True


def test_superuser(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(
        email=fake_email, password=fake_password, is_superuser=True)
    user = user_crud.create(db, obj_in=user_in)

    # Act
    is_superuser = user_crud.is_superuser(user)

    # Assert
    assert is_superuser is True


def test_user_that_is_not_superuser(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)

    # Act
    is_superuser = user_crud.is_superuser(user)

    # Assert
    assert is_superuser is False


def test_get_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(
        email=fake_email, password=fake_password, is_superuser=True)
    user = user_crud.create(db, obj_in=user_in)

    # Acr
    retrieved_user = user_crud.get(db, id=user.id)

    # Assert
    assert retrieved_user
    assert user.email == retrieved_user.email
    assert jsonable_encoder(user) == jsonable_encoder(retrieved_user)


def test_update_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_users: None
) -> None:
    # Arrange
    user_in = UserCreate(
        email=fake_email,
        password=fake_password,
        is_superuser=True
    )
    user = user_crud.create(db, obj_in=user_in)

    # Act
    new_password = 'new_p@ssword'
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    user_crud.update(db, db_obj=user, obj_in=user_in_update)
    retrieved_user = user_crud.get(db, id=user.id)

    # Assert
    assert retrieved_user
    assert user.email == retrieved_user.email
    assert verify_password(new_password, retrieved_user.hashed_password)
