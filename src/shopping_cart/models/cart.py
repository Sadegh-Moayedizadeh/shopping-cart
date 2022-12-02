from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey

from shopping_cart.db import Base


class Cart(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship('User', back_populates='cart', uselist=False)
    products = relationship('Product', back_populates='cart')
