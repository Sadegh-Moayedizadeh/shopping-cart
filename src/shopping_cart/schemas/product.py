from typing import List, Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    cart_id: Optional[int] = None


class ProductInDBBase(ProductBase):
    id: int = None
    cart_id: Optional[int] = None

    class Config:
        orm_mode = True


class Product(ProductInDBBase):
    pass


class ProductInDB(ProductInDBBase):
    pass
