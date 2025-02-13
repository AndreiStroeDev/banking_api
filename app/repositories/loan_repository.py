from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.loan import Loan

class LoanRepository:
    @staticmethod
    async def create_loan(db: AsyncSession, loan: Loan):
        db.add(loan)
        await db.commit()
        await db.refresh(loan)
        return loan
    
    @staticmethod
    async def get_loans_by_user(db: AsyncSession, user_id:int):
        result = await db.execute(select(Loan).filter(Loan.user_id == user_id))
        return result.scalars().all()