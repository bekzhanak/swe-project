from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_available_products, search_products, filter_products, create_buyer, authenticate_user, get_buyer_by_user_id, get_product_by_id, create_order
from database import get_db
from schemas import BuyerCreate, LoginRequest, BuyerResponse, ProductResponse, OrderResponse, OrderCreate
from dependencies import create_access_token, get_current_user
from models import User
from typing import List, Optional

router = APIRouter()


@router.post("/register")
def register_buyer(buyer_data: BuyerCreate, db: Session = Depends(get_db)):
    create_buyer(db, buyer_data)
    return {"message": "buyer registered successfully"}


@router.post("/login")
def login_buyer(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request.email, login_request.password)
    if user is None:
        raise HTTPException(status_code=403, detail="User does not exist")
    buyer = get_buyer_by_user_id(db, user.id)
    if buyer is None:
        raise HTTPException(status_code=403, detail="user is not buyer")
    access_token = create_access_token({"sub": user.email, "role": "admin" if user.is_admin else "user"})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model=BuyerResponse)
def get_buyer_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    buyer = get_buyer_by_user_id(db, current_user.id)
    if buyer is None:
        raise HTTPException(status_code=403, detail="User is not buyer")
    return buyer


@router.get("/products")
def browse_products(db: Session = Depends(get_db)):
    return get_available_products(db)


@router.get("/products/{product_id}")
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(db, product_id)


@router.get("/products/search")
def search_products_endpoint(query: str, db: Session = Depends(get_db)):
    return search_products(db, query)


@router.get("/products/filter")
def filter_products_endpoint(price_range: Optional[str] = None, category: Optional[int] = None, db: Session = Depends(get_db)):
    return filter_products(db, price_range, category)


@router.post("/orders", response_model=OrderResponse)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    buyer = get_buyer_by_user_id(db, current_user.id)
    if not buyer:
        raise HTTPException(status_code=403, detail="User is not a buyer")
    order_data.buyer_id = buyer.id
    order = create_order(db, order_data)
    return order


@router.get("/orders", response_model=List[OrderResponse])
def get_buyer_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    buyer = get_buyer_by_user_id(db, current_user.id)
    if not buyer:
        raise HTTPException(status_code=403, detail="User is not a buyer")
    return buyer.orders
