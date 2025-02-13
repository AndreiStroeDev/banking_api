from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transaction_schema import DepositRequest, TransferRequest, TransactionResponse
from app.models.user import User
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.utils.dependencies import get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/deposit/", response_model=TransactionResponse)
async def deposit(request: DepositRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Handles deposit transactions for authenticated users"""
    transaction_service = TransactionService(db)
    return await transaction_service.deposit(
        user_id=user.id,
        account_id=request.account_id,
        amount=request.amount
    )

@router.post("/withdraw/", response_model=TransactionResponse)
async def withdraw(request: DepositRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Handles withdrawal transactions for authenticated users"""
    transaction_service = TransactionService(db)
    return await transaction_service.withdraw(
        user_id=user.id,
        account_id=request.account_id,
        amount=request.amount
    )

@router.post("/transfer/")
async def transfer(request: TransferRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    """Handles transfer transactions for authenticated users"""
    transaction_service = TransactionService(db)
    return await transaction_service.transfer(
        sender_id=user.id,
        receiver_account_id=request.receiver_account_id,
        amount=request.amount
    )