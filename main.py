from fastapi import FastAPI, Depends
from app.database import engine, get_db
from app.models.base import Base
from app.api import auth, accounts, transactions, loans
# from sqlalchemy.orm import Session
# from sqlalchemy import text

app = FastAPI(title="Banking API", debug=True)

Base.metadata.create_all(bind=engine)

# @app.get("/")
# def test_connection(db: Session = Depends(get_db)):
#     try:
#         db.execute(text("SELECT 1"))
#         return {"message": "Database connection is working!"}
#     except Exception as e:
#         return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "Welcome to the Banking API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])
