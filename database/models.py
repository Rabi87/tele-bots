from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, index=True)
    email = Column(String(120), unique=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    balance = Column(Float(precision=2), default=0.0)
    referral_code = Column(String(20), unique=True)
    created_at = Column(DateTime(timezone=True), server_default='now()')

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    category = Column(String(20))  # proxy/phone
    name = Column(String(50), unique=True)
    price = Column(Float(precision=2))
    stock = Column(Integer, default=0)

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float(precision=2))
    type = Column(String(10))  # deposit/purchase
    timestamp = Column(DateTime(timezone=True), server_default='now()')