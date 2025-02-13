from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import UserNotFoundException, UserAlreadyExistsException

class UserService:
    def __init__(self, db:AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate, is_admin=False):
        existing_user = await UserRepository.get_user_by_email(self.db, user_data.email)
        if existing_user:
            raise UserAlreadyExistsException()
        
        new_user = User(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hash_password(user_data.password),
            is_admin = is_admin
        )
        
        created_user = await UserRepository.create_user(self.db, new_user)
        return created_user
    
    async def get_user_id_by_email(self, email: str) -> int:
        user = await UserRepository.get_user_by_email(self.db, email)
        if not user:
            raise UserNotFoundException()
        return user.id