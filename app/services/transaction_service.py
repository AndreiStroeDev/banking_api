from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository
from app.models.transaction import Transaction
from app.utils.exceptions import AccountNotFoundException, InsufficientFundsException

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def deposit(self, user_id: int, account_id: int, amount: float) -> Transaction:
        account = await AccountRepository.get_account_by_id(self.db, account_id)
        if not account or account.user_id != user_id:
            raise AccountNotFoundException()

        transaction = Transaction(
            user_id=user_id,
            account_id=account_id,
            type="deposit",
            amount=amount
        )
        await TransactionRepository.record_transaction(self.db, transaction)
        
        account.balance += amount
        await self.db.commit()
        
        return transaction

    async def withdraw(self, user_id: int, account_id: int, amount: float) -> Transaction:
        account = await AccountRepository.get_account_by_id(self.db, account_id)
        if not account or account.user_id != user_id:
            raise AccountNotFoundException()

        if account.balance < amount:
            raise InsufficientFundsException()

        transaction = Transaction(
            user_id=user_id,
            type="withdrawal",
            amount=amount
        )
        await TransactionRepository.record_transaction(self.db, transaction)
        
        account.balance -= amount
        await self.db.commit()
        return transaction

    async def transfer(self, sender_id, sender_account_id: int, receiver_account_id: int, amount: float) -> dict:
        sender_account = await AccountRepository.get_account_by_user_id(self.db, sender_account_id)
        receiver_account = await AccountRepository.get_account_by_id(self.db, receiver_account_id)

        if not sender_account or not receiver_account:
            raise AccountNotFoundException()

        if sender_account.balance < amount:
            raise InsufficientFundsException()

        # Deduct from sender
        sender_transaction = Transaction(
            user_id=sender_id,
            type="transfer_out",
            amount=amount
        )
        await TransactionRepository.record_transaction(self.db, sender_transaction)
        sender_account.balance -= amount
        
        # Credit to receiver
        receiver_transaction = Transaction(
            user_id=receiver_account.user_id,
            type="transfer_in",
            amount=amount
        )
        await TransactionRepository.record_transaction(self.db, receiver_transaction)
        receiver_account.balance += amount

        await self.db.commit()
        return {
            "message": f"Transferred {amount} from Account {sender_account.id} to Account {receiver_account.id}"
        }
