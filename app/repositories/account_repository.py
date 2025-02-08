from sqlalchemy.orm import Session
from app.models.account import Account

class AccountRepository:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account:
        return db.query(Account).filter(Account.id == account_id).first()

    @staticmethod
    def get_account_by_user_id(db: Session, user_id: int) -> Account:
        return db.query(Account).filter(Account.user_id == user_id).first()
