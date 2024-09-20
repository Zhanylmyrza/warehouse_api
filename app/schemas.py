from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    name: str
    description: str
    price: float
    stock: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


class OrderStatus(str, Enum):
    pending = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class OrderCreate(BaseModel):
    status: OrderStatus
    items: List[int]


class Order(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    items: List[int]

    class Config:
        from_attributes = True
