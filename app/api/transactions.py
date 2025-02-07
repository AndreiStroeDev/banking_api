from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.transaction_schema import DepositRequest, TransferRequest
from app.database import get_db

router = APIRouter()

@router.post("/deposit/")
def deposit(request: DepositRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    response = account.deposit(request.amount)
    db.commit()
    return response

@router.post("/withdraw/")
def withdraw(request: DepositRequest, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == request.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    response = account.withdraw(request.amount)
    db.commit()
    return response

@router.post("/transfer/")
def transfer(request: TransferRequest, db: Session = Depends(get_db)):
    sender = db.query(Account).filter(Account.id == request.sender_id).first()
    receiver = db.query(Account).filter(Account.id == request.receiver_id).first()
    
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Invalid sender/receiver account")
    
    if sender.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    sender.withdraw(request.amount)
    receiver.deposit(request.amount)
    db.commit()

    return {"message": f"Transfered {request.amount} from Account {sender.id} to Account {receiver.id}"}