from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    phone_number: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(UserBase):
    id: int
    is_admin: bool
    is_buyer: bool
    is_farmer: bool
    is_active: bool

    class Config:
        from_attributes = True


# Farmer schemas
class FarmerCreate(UserCreate):
    farm_address: str
    farm_size: float


class FarmResponse(BaseModel):
    id: int
    address: str
    size: int

    class Config:
        from_attributes = True


class FarmerResponse(BaseModel):
    id: int
    farms: List[FarmResponse]
    user: UserResponse

    class Config:
        from_attributes = True


# Buyer schemas
class BuyerCreate(UserCreate):
    address: str
    payment_method: str


class BuyerResponse(BaseModel):
    id: int
    address: str
    payment_method: str
    user: UserResponse

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    category_id: int


class ProductResponse(ProductCreate):
    farmer: FarmerResponse


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    buyer_id: Optional[int] = None
    date: datetime
    amount: float
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    buyer_id: int
    date: datetime
    status: str
    amount: float
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PaymentRequest(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    payment_reference: Optional[str] = None


class MoneyRequest(BaseModel):
    id: int
    amount: float