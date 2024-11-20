from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, Boolean, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    phone_number = Column(String(20), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    farmers = relationship('Farmer', back_populates='user')
    buyers = relationship('Buyer', back_populates='user')
    is_buyer = Column(Boolean, default=False)
    is_farmer = Column(Boolean, default=False)
    balance = Column(Float, nullable=False, default=0.0)


class Farmer(Base):
    __tablename__ = 'farmers'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='farmers')
    farms = relationship('Farm', back_populates='farmer')
    products = relationship('Product', back_populates='farmer')
    pending = Column(Boolean, default=True)


class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), nullable=True)
    payment_method = Column(String(20), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='buyers')
    orders = relationship('Order', back_populates='buyer')


class Farm(Base):
    __tablename__ = 'farms'
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    address = Column(String(255), nullable=True)
    size = Column(Float, nullable=True)
    government_id = Column(Integer, nullable=True)
    farmer = relationship('Farmer', back_populates='farms')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    price = Column(DECIMAL(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')
    farmer = relationship('Farmer', back_populates='products')


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    date = Column(TIMESTAMP, nullable=True)
    status = Column(String, nullable=True)
    amount = Column(Integer, nullable=True)
    buyer = relationship('Buyer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')
    payments = relationship('Payment', back_populates='order')
    deliveries = relationship('Delivery', back_populates='order')


class OrderItem(Base):
    __tablename__ = 'orderItems'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order = relationship('Order', back_populates='items')
    product = relationship('Product')


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    date = Column(TIMESTAMP, nullable=True)
    amount = Column(Integer, nullable=False)
    status = Column(String, nullable=True)
    order = relationship('Order', back_populates='payments')


class Delivery(Base):
    __tablename__ = 'deliveries'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    date = Column(TIMESTAMP, nullable=True)
    status = Column(String, nullable=True)
    delivery_address = Column(String(255), nullable=True)
    order = relationship('Order', back_populates='deliveries')
