# db.py

import uuid
from datetime import datetime
from collections.abc import AsyncGenerator

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Async SQLite URL
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Session maker
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Base class (new style)
class Base(DeclarativeBase):
    pass


# Models
class Post(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)  # simpler than UUID for now
    title = Column(String, index=True)
    content = Column(String)
    caption = Column(String)


class FilePost(Base):
    __tablename__ = "file_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
# call this on app startup

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session