from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    product_ids: List[int] = []


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserProductIds(BaseModel):
    product_ids: List[int]


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
