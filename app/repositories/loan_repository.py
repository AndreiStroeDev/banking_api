from sqlalchemy.orm import Session
from app.models.loan import Loan

class LoanRepository:
    @staticmethod
    def create_loan(db: Session, loan: Loan):
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan
    
    @staticmethod
    def get_loans_by_user(db: Session, user_id:int):
        return db.query(Loan).filter(Loan.user_id == user_id).all()