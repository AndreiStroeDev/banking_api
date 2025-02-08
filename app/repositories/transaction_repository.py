from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction

class TransactionRepository:
    @staticmethod
    def record_transaction(db: Session, transaction: Transaction):
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_transactions_by_user(db: Session, user_id: int):
        return db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    @staticmethod
    def get_balance(db: Session, user_id: int):
        deposits = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type.in_(["deposit", "transfer_in"])
        ).scalar() or 0

        withdrawals = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type.in_(["withdrawal", "transfer_out"])
        ).scalar() or 0

        return deposits - withdrawals