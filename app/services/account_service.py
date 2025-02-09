from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.account import Account
from app.schemas.account_schema import AccountCreate
from app.repositories.account_repository import AccountRepository

class AccountService:
    def __init__(self, db: Session):
        self.db = db

    def create_account(self, account_data: AccountCreate):
        existing_account = self.db.query(Account).filter(
            Account.user_id == account_data.user_id,
            Account.account_type == account_data.account_type
        ).first()

        if existing_account:
            raise HTTPException(status_code=409, detail=f"User already has a {account_data.account_type} account")
        
        new_account = Account(
            user_id=account_data.user_id,
            account_type=account_data.account_type,
            balance=account_data.balance
        )

        return new_account