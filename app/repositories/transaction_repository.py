from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import case, func
from app.models.transaction import Transaction

class TransactionRepository:
    @staticmethod
    async def record_transaction(db: AsyncSession, transaction: Transaction):
        if transaction.account_id is None:
            raise ValueError("Transaction must be linked to an account")
        
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction
    
    @staticmethod
    async def get_transactions_by_user(db: AsyncSession, user_id: int):
        result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_transaction_by_account(db: AsyncSession, account_id: int):
        result = await db.execute(select(Transaction).filter(Transaction.account_id == account_id))
        return result.scalars().all()
    
    @staticmethod
    async def get_balance(db: AsyncSession, account_id: int):
        deposits = await db.execute(
            select(func.sum(Transaction.amount))
            .filter(Transaction.account_id == account_id,
                    Transaction.type.in_(["deposit", "transfer_in"]))
        ).scalar() or 0

        withdrawals = await db.execute(
            select(func.sum(Transaction.amount))
            .filter(Transaction.account_id == account_id,
                    Transaction.type.in_(["withdrawal", "transfer_out"]))
        ).scalar() or 0

        return deposits - withdrawals

    # @staticmethod
    # def get_balance(db:AsyncSession, account_id: int):
    #     balance = db.query(
    #         func.sum(
    #             case(
    #                 [(Transaction.type.in_(["deposit", "transfer_in"]), Transaction.amount)],
    #                 [(Transaction.type.in_(["withdrawal", "transfer_out"]), -Transaction.amount)],
    #                 else_=0
    #             )
    #         )
    #     ).filter(Transaction.account_id == account_id).scalar() or 0

    #     return balance