from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):  
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # SERIAL in SQL maps to Integer + auto increment
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(20), default="customer")  # 'customer' or 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)  # auto-set on insert
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # auto-update on change