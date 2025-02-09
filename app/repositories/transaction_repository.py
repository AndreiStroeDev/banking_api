from sqlalchemy.orm import Session
from sqlalchemy import case, func
from app.models.transaction import Transaction

class TransactionRepository:
    @staticmethod
    def record_transaction(db: Session, transaction: Transaction):
        if transaction.account_id is None:
            raise ValueError("Transaction must be linked to an account")
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    
    @staticmethod
    def get_transactions_by_user(db: Session, user_id: int):
        return db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    @staticmethod
    def get_transaction_by_account(db: Session, account_id: int):
        return db.query(Transaction).filter(Transaction.account_id == account_id).all()
    
    # @staticmethod
    # def get_balance(db: Session, user_id: int):
    #     deposits = db.query(func.sum(Transaction.amount)).filter(
    #         Transaction.user_id == user_id,
    #         Transaction.type.in_(["deposit", "transfer_in"])
    #     ).scalar() or 0

    #     withdrawals = db.query(func.sum(Transaction.amount)).filter(
    #         Transaction.user_id == user_id,
    #         Transaction.type.in_(["withdrawal", "transfer_out"])
    #     ).scalar() or 0
    @staticmethod
    def get_balance(db:Session, account_id: int):
        balance = db.query(
            func.sum(
                case(
                    [(Transaction.type.in_(["deposit", "transfer_in"]), Transaction.amount)],
                    [(Transaction.type.in_(["withdrawal", "transfer_out"]), -Transaction.amount)],
                    else_=0
                )
            )
        ).filter(Transaction.account_id == account_id).scalar() or 0

        return balance