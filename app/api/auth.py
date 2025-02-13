from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/signup/", response_model=UserResponse)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    new_user = await user_service.create_user(user)
    return new_user

@router.post("/login/")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token, expiry = await auth_service.authenticate_user(user)
    
    return {"access_token": token, "token_type": "bearer", "expires_in": expiry}

@router.get("/users/me")
async def get_current_user_profile(user_email: str = Depends(get_current_user)) -> dict:
    return {"message": "User authenticated", "email": user_email}