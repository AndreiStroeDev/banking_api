from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.models.user import User
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/signup/", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    new_user = user_service.create_user(user)

    return new_user

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    token, expiry = auth_service.authenticate_user(user)
    return {"access_token": token, "token_type": "bearer", "expires_in": expiry}

@router.get("/users/me")
def get_current_user_profile(user: str = Depends(get_current_user)):
    return user