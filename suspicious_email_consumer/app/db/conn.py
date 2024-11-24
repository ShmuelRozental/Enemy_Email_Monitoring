from .models import Base
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL =  "postgresql+asyncpg://postgres:1234@postgres/email_monitor"


engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    print('Trying to initialize the database...')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
