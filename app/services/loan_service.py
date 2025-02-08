from sqlalchemy.orm import Session
from app.schemas.loan_schema import LoanRequest
from app.models.loan import Loan
from app.repositories.loan_repository import LoanRepository

class LoanService:
    def __init__(self, db:Session):
        self.db = db

    def apply_for_loan(self, user_id: int, loan_data: LoanRequest):
        new_loan = Loan(
            user_id = user_id,
            amount = loan_data.amount,
            duration_months = loan_data.duration_months
        )

        return LoanRepository.create_loan(self.db, new_loan)
    
    def get_user_loans(self, user_id: int):
        return LoanRepository.get_loans_by_user(self.db, user_id)