from fastapi import HTTPException

class InsufficientFundsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Insufficient funds")

class AccountNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Account not found")

class UnauthorizedAccessException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Unauthorized access to this account")
