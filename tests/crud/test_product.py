from sqlalchemy.orm import Session

from shopping_cart.crud import product_crud
from shopping_cart.schemas import ProductCreate, ProductUpdate


def test_create(db: Session) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )

    # Act
    product = product_crud.create(db=db, obj_in=product_in)

    # Assert
    assert product.title == 'fake_title'
    assert product.price == 0
    assert product.category == 'fake_category'
    assert product.description == 'fake_description'
    assert product.image == 'fake_image_address'


def test_get(db: Session) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )

    # Act
    product = product_crud.create(db=db, obj_in=product_in)
    stored_product = product_crud.get(db=db, id=product.id)

    # Assert
    assert product == stored_product


def test_update(db: Session) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )
    product_update_in = ProductUpdate(title='alternative_fake_title')

    # Act
    product = product_crud.create(db=db, obj_in=product_in)
    updated_product = product_crud.update(
        db=db,
        db_obj=product,
        obj_in=product_update_in
    )

    # Assert
    assert updated_product.id == product.id
    assert updated_product.title == 'alternative_fake_title'


def test_delete(db: Session) -> None:
    # Arrange
    product_in = ProductCreate(
        title='fake_title',
        price=0,
        category='fake_category',
        description='fake_description',
        image='fake_image_address'
    )
    product_update_in = ProductUpdate(title='alternative_fake_title')

    # Act
    product = product_crud.create(db=db, obj_in=product_in)
    product_crud.remove(db=db, id=product.id)
    stored_product = product_crud.get(db=db, id=product.id)

    # Assume
    assert product

    # Assert
    assert stored_product is None
