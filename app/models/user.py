from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    accounts = relationship("Account", back_populates="user", cascade="all, delete")
    loans = relationship("Loan", back_populates="user", cascade="all, delete")
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete")