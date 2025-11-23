import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import text
from fastapi import Depends

load_dotenv()

POSTGRES_USER     = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST     = os.getenv("POSTGRES_HOST")
POSTGRES_PORT     = os.getenv("POSTGRES_PORT")
POSTGRES_DB       = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Connect to database
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def main():
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL, echo=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connection works:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)
    get_db()

if __name__ == "__main__":
    main()