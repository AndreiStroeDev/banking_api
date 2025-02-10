from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.services.user_service import User
from app.database import get_db
from app.config.settings import settings
from app.utils.exceptions import UserNotFoundException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def decode_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_jwt(token)
    user_email: str = payload.get("sub")

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user_service = UserService(db)
    user = user_service.get_user_id_by_email(user_email)
    if not user:
        raise UserNotFoundException()
    
    return user