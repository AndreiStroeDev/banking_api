from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.loan_schema import LoanRequest, LoanResponse
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.utils.dependencies import get_current_user

router = APIRouter()

@router.post("/apply/", response_model=LoanResponse)
def apply_for_loan(request: LoanRequest, db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    user_service = UserService(db)
    user_id = user_service.get_user_id_by_email(user_email)
    loan_service = LoanService(db)
    new_loan = loan_service.apply_for_loan(user_id, request)
    return new_loan

@router.get("/", response_model=list[LoanResponse])
def get_user_loans(db: Session = Depends(get_db), user_email: str = Depends(get_current_user)):
    user_service = UserService(db)
    user_id = user_service.get_user_id_by_email(user_email)
    loan_service = LoanService(db)
    return loan_service.get_user_loans(user_id)