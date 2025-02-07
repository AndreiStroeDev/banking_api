from pydantic import BaseModel

class DepositRequest(BaseModel):
    account_id: int
    amount: float

class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: float