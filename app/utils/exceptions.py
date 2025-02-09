from fastapi import HTTPException

class InsufficientFundsException(HTTPException):
    def __init__(self, balance: float, amount: float):
        super().__init__(status_code=400, detail=f"Insufficient funds: Tried to withdraw {amount}, but balance is {balance}")

class AccountNotFoundException(HTTPException):
    def __init__(self, account_id: int):
        super().__init__(status_code=404, detail=f"Account with ID {account_id} not found")

class UnauthorizedAccessException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Unauthorized access to this account")

class UserNotFound(HTTPException):
    def __init__(self, email: str = None):
        detail = f"User with email {email} not found" if email else "User not found"
        super().__init__(status_code=404, detail=detail)

class NoAccountsForUser(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=409, detail=f"No accounts found for user with ID {user_id}")
