from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account_schema import AccountCreate, AccountResponse
from app.models.account import Account
from app.models.user import User
from app.database import get_db

router = APIRouter()

@router.post("/create/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == account.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_account = Account(user_id=account.user_id, account_type=account.account_type, balance=account.balance)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.get("/{user_id}/accounts/", response_model=list[AccountResponse])
def get_user_account(user_id: int, db: Session = Depends(get_db)):
    accounts = db.query(Account).filter(Account.user_id == user_id).all()

    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for this user")
    return accounts