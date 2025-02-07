from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user import User
from app.services.auth_services import hash_password, create_access_token, verify_password
from app.database import get_db
import logging

logger = logging.getLogger("uvicorn.error")

router = APIRouter()

@router.post("/signup/", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hash_password=hashed_pw)
   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return {"error": "Invalid credentials"}
    
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}