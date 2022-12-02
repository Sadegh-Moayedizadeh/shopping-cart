from typing import List, Optional

from pydantic import BaseModel


class CartBase(BaseModel):
    pass


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    pass


class CartInDBBase(CartBase):
    id: int = None
    owner_id: int = None

    class Config:
        orm_mode = True


class Cart(CartInDBBase):
    pass


class CartInDB(CartInDBBase):
    pass
