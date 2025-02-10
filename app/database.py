from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

DATABASE_URL = settings.DATABASE_URL.replace("postgresql", "postgresql+asyncpg")

async_engine = create_async_engine(DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(
    async_engine, 
    expire_on_commit=False, 
    class_=AsyncSession
    )

async def get_db():
    async with async_session() as session:
        yield session