from pydantic import BaseModel

class TransactionBase(BaseModel):
    type: str  # "deposit", "withdrawal", or "transfer"
    amount: float

class DepositRequest(TransactionBase):
    account_id: int

class TransferRequest(BaseModel):
    receiver_account_id: int
    amount: float

class TransactionResponse(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True