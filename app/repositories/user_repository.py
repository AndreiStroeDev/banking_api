from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

class UserRepository:
    @staticmethod
    async def get_user_by_id(db:AsyncSession, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)

        return result.scalars().first()
    
    @staticmethod
    async def get_user_by_email(db:AsyncSession, email: str):
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)

        return result.scalars().first()
    
    @staticmethod
    async def create_user(db:AsyncSession, user: User):
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete_user(db:AsyncSession, user_id: int):
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if user:
            await db.delete(user)
            await db.commit()