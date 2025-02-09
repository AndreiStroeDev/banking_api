from pydantic import BaseModel

class LoanRequest(BaseModel):
    amount: float
    duration_months: int

class LoanResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    interest_rate: float
    duration_months: int
    is_paid: bool
    
    class Config:
        from_attributes = True