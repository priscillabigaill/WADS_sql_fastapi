from typing import List, Optional

from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str

class ItemCreate(ItemBase):
    owner_id: int

class ItemUpdate(BaseModel):
    title: Optional[str] = None

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
