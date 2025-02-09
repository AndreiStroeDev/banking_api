from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserLogin
from app.utils.security import verify_password, create_access_token
from fastapi import HTTPException

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def authenticate_user(self, login_data: UserLogin):
        db_user = self.db.query(User).filter(User.email == login_data.email).first()

        if not db_user or not verify_password(login_data.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        token = create_access_token({"sub": db_user.email})

        return {"access_token": token, "token_type": "bearer"}