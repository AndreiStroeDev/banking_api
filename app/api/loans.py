from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.loan import Loan
from app.models.user import User
from app.schemas.loan_schema import LoanRequest
from app.database import get_db

router = APIRouter()

@router.post("/apply/")
def apply_for_loan(request: LoanRequest, db: Session = Depends(get_db)):
    loan = Loan(user_id=request.user_id, amount=request.amount, duration_months=request.duration)

    db.add(loan)
    db.commit()
    db.refresh(loan)

    return {"message": "Loan application successful", "loan_id": loan.id}

@router.get("/{user_id}/")
def get_user_loan(user_id: int, db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return loans