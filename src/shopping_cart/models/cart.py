from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from shopping_cart.db import Base


class Cart(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User", back_populates='cart', uselist=False)
    products = relationship('Product')
