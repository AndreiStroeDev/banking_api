from sqlalchemy import Column, Integer, ForeignKey, Float, Boolean
from app.models.base import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, default=0.06)
    duration_months = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)

    def calculate_total_amount(self):
        return self.amount * (1 + self.interest_rate * (self.duration_month / 12))