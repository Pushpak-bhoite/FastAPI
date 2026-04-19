# db.py

import uuid
from datetime import datetime
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy import Column, ForeignKey, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
#for user 
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID


# Async SQLite URL
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

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


class User(SQLAlchemyBaseUserTableUUID, Base): ###################***
    File_Posts = relationship("FilePost", back_populates="user")
    assets = relationship("Asset", back_populates="user")
    
class FilePost(Base):
    __tablename__ = "file_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # make relationship with User as FK (makes one to many relation)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"),  nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Connects tables 
    user = relationship("User", back_populates="File_Posts")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    asset_type = Column(String, nullable=False)  # "http", "ssl", "ping", "port", "dns"
    target = Column(String, nullable=False)  # URL/domain/IP
    port = Column(String, nullable=True)
    status = Column(String, default="unknown")  # "up", "down", "unknown"
    last_checked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    
    user = relationship("User", back_populates="assets")
    
    
# call this on app startup
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)
    
    
