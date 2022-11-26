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
    delete_user_by_email: None
) -> None:
    email = fake_email
    password = fake_password
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    email = fake_email
    password = fake_password
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)
    authenticated_user = user_crud.authenticate(
        db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_non_existing_user_should_not_authenticate(
    db: Session,
    fake_email: str,
    fake_password: str
) -> None:
    email = fake_email
    password = fake_password
    user = user_crud.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    email = fake_email
    password = fake_password
    user_in = UserCreate(email=email, password=password)
    user = user_crud.create(db, obj_in=user_in)
    is_active = user_crud.is_active(user)
    assert is_active is True


def test_disabled_user_should_be_active(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    email = fake_email
    password = fake_password
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = user_crud.create(db, obj_in=user_in)
    is_active = user_crud.is_active(user)
    assert is_active


def test_superuser(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    user_in = UserCreate(email=fake_email, password=fake_password, is_superuser=True)
    user = user_crud.create(db, obj_in=user_in)
    is_superuser = user_crud.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    user_in = UserCreate(email=fake_email, password=fake_password)
    user = user_crud.create(db, obj_in=user_in)
    is_superuser = user_crud.is_superuser(user)
    assert is_superuser is False


def test_get_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    user_in = UserCreate(email=fake_email, password=fake_password, is_superuser=True)
    user = user_crud.create(db, obj_in=user_in)
    user_2 = user_crud.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(
    db: Session,
    fake_email: str,
    fake_password: str,
    delete_user_by_email: None
) -> None:
    user_in = UserCreate(email=fake_email, password=fake_password, is_superuser=True)
    user = user_crud.create(db, obj_in=user_in)
    new_password = 'new_p@ssword'
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    user_crud.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = user_crud.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)
