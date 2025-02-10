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

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class NoAccountsForUserException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="No accounts found for this user")
