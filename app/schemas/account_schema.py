from pydantic import BaseModel
from enum import Enum

class AccountType(str, Enum):
    savings="savings"
    checking="checking"
    investment="investment"

class AccountCreate(BaseModel):
    user_id: int
    account_type: AccountType
    balance: float = 0.0

class AccountResponse(BaseModel):
    id: int
    user_id: int
    account_type: AccountType
    balance: float = 0.0

    class Config:
        from_attributes = True