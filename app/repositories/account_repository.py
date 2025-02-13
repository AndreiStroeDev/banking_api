from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.account import Account

class AccountRepository:    
    @staticmethod
    async def get_account_by_id(db: AsyncSession, account_id: int) -> Account | None:
        result = await db.execute(select(Account).filter(Account.id == account_id))
        return result.scalars().first()

    @staticmethod
    async def get_account_by_user_id(db: AsyncSession, user_id: int) -> list[Account]:
        result = await db.execute(select(Account).filter(Account.user_id == user_id))
        return result.scalars().all()
    
    @staticmethod
    async def create_account(db: AsyncSession, account: Account) -> Account:
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account
        
