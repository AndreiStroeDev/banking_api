from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.services.account_service import AccountService
from app.models.account import Account
from app.models.user import User
from app.utils.exceptions import UserNotFoundException, NoAccountsForUserException
from app.utils.dependencies import get_current_user
from app.database import get_db

router = APIRouter()

@router.post("/create/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    account_service = AccountService(db)
    return account_service.create_account(account)

@router.get("/{user_id}/accounts/", response_model=list[AccountResponse])
def get_user_account(db: Session = Depends(get_db), user=Depends(get_current_user)):
    account_service = AccountService(db)
    return account_service.get_accounts_by_user(user.id)