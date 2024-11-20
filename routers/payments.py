from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Payment, Order, Delivery, Buyer, User
from schemas import PaymentRequest, MoneyRequest
from datetime import datetime

router = APIRouter()

@router.post("/payments")
def process_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == payment.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    buyer = db.query(Buyer).filter(Buyer.id == order.buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    user = db.query(User).filter(User.id == buyer.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    if payment.amount < order.amount:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")

    if user.balance < payment.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    user.balance -= payment.amount

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    for item in order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        farmer = db.query(Farmer).filter(Farmer.id == product.farmer_id).first()
        if not farmer:
            raise HTTPException(status_code=404, detail=f"Farmer not found for product {product.id}")

        user = db.query(User).filter(User.id == farmer.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        farmer_share = item.price * item.quantity
        user.balance += farmer_share

    payment_record = Payment(
        order_id=payment.order_id,
        date=datetime.utcnow(),
        amount=payment.amount,
        status="Processed",
    )
    db.add(payment_record)
    db.commit()
    db.refresh(payment_record)

    delivery = Delivery(
        order_id=order.id,
        date=datetime.utcnow(),
        status="Pending",
        delivery_address=buyer.address,
    )
    db.add(delivery)
    db.commit()
    db.refresh(delivery)

    return {
        "message": "Payment processed successfully, delivery initiated",
        "payment_id": payment_record.id,
        "delivery_id": delivery.id
    }


@router.post("/deposit")
def deposit_money(deposit: MoneyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == deposit.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if deposit.amount <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be greater than zero")

    user.balance += deposit.amount
    db.commit()
    db.refresh(user)

    return {
        "message": "Deposit successful",
        "user_id": user.id,
        "updated_balance": user.balance
    }


@router.post("/withdraw")
def withdraw_money(withdrawal: MoneyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == withdrawal.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if withdrawal.amount <= 0:
        raise HTTPException(status_code=400, detail="Withdrawal amount must be greater than zero")
    if user.balance < withdrawal.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    user.balance -= withdrawal.amount
    db.commit()
    db.refresh(user)

    return {
        "message": "Withdrawal successful",
        "buyer_id": user.id,
        "updated_balance": user.balance
    }