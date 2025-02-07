from pydantic import BaseModel

class LoanRequest(BaseModel):
    user_id: int
    amount: float
    duration: int

class LoanResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    interest_rate: float
    duration_months: int
    is_paid: bool
    
    class Config:
        from_attributes = True