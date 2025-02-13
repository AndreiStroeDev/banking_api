from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user_schema import UserLogin
from app.utils.security import verify_password, create_access_token
from fastapi import HTTPException
from app.config.settings import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(self, login_data: UserLogin):
        db_user = await self.db.execute(
            select(User).where(User.email == login_data.email)
        )
        db_user = db_user.scalar_one_or_none()

        if not db_user or not verify_password(login_data.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        expiry_time = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        token = create_access_token({"sub": db_user.email})

        return token, expiry_time