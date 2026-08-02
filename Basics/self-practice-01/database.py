from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://postgres:PB%40supabase123@db.gngvbplntcyedbtplcrk.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL,  echo="debug") # here we create engine object, and connection pool
#echo="debug" Shows connection checkout/checkin

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# ========= DB generator function =============
def get_db() -> Generator:
    db = SessionLocal() # here session asks the engine for a connection from pool. 
    try: 
        yield db #when we call db.close connection is returned to pool 
    finally:
        db.close()