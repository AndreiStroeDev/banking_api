from fastapi import FastAPI, Depends
from app.database import async_engine, get_db
from app.models.base import Base
from app.api import auth, accounts, transactions, loans
# from sqlalchemy.orm import Session
# from sqlalchemy import text

app = FastAPI(title="Banking API", debug=True)

# Base.metadata.create_all(bind=async_engine)
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])

if __name__ == "__main__":
    import uvicorn
    import asyncio
    
    async def app_startup():
        await create_tables()
        uvicorn.run(app, host="localhost", port=8000)

    asyncio.run(app_startup())
