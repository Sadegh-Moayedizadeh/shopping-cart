from sqlalchemy import Boolean, Column, Integer, String, Float, Enum, Binary
from sqlalchemy.orm import relationship
from enum import Enum

from shopping_cart.db import Base


class Category(Enum):
    ELECTRONICS = "electronics",
    JWELERY = "jewelery",
    MENS_CLOTHING = "men's clothing",
    WOMENS_CLOTHING = "women's clothing"


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float, nullable=False)
    category = Column(Enum(Category), nullable=True)
    description = Column(String)
    image = Column(Binary, nullable=True)
