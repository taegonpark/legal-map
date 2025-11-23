from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

DATABASE_URL = "postgresql://user:password@localhost:5432/legal_map"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Connect to database
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()