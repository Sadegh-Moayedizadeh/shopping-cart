from sqlalchemy import ARRAY, Boolean, Column, Integer, String, Float
from sqlalchemy.orm import relationship

from shopping_cart.db import Base


class Product(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Float)
    category = Column(String)
    description = Column(String)
    image = Column(String)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    cart = relationship('Cart', back_populates='products')
