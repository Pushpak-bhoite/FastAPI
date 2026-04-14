# sqlAlchemy - is a orm for python 

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQLite database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Post model
class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    caption = Column(String) ###############

class FilePost(Base):
    __tablename__ = "file_posts"

    id= Column(Integer, primary_key=True, index=True)
    caption = Column(String)
    url = Column(String)
    file_type= Column(String)
    file_name = Column(String)
    created_At= Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()