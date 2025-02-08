from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transaction_schema import DepositRequest, TransferRequest, TransactionResponse
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.utils.dependencies import get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/deposit/", response_model=TransactionResponse)
def deposit(request: DepositRequest, db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    """Handles deposit transactions for authenticated users"""
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    user_id = user_service.get_user_id_by_email(user_email)
    return transaction_service.deposit(user_id=user_id, account_id=request.account_id, amount=request.amount)

@router.post("/withdraw/", response_model=TransactionResponse)
def withdraw(request: DepositRequest, db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    """Handles withdrawal transactions for authenticated users"""
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    user_id = user_service.get_user_id_by_email(user_email) 
    return transaction_service.withdraw(user_id=user_id, account_id=request.account_id, amount=request.amount)

@router.post("/transfer/")
def transfer(request: TransferRequest, db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    """Handles transfer transactions for authenticated users"""
    transaction_service = TransactionService(db)
    user_service = UserService(db)
    sender_id = user_service.get_user_id_by_email(user_email)
    return transaction_service.transfer(
        sender_id=sender_id, 
        receiver_account_id=request.receiver_account_id, 
        amount=request.amount
    )