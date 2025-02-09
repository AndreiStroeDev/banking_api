from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete")

    def deposit(self, amount: float):
        self.balance += amount
        return {"message": f"Deposited {amount}. New Balance: {self.balance}"}
    
    def withdraw(self, amount: float):
        if amount > self.balance:
            return {"message": "Insufficient funds"}
        self.balance -= amount
        return {"message": f"Withdrew {amount}. New Balance: {self.balance}"}