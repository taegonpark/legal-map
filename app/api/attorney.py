from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import Attorney
from db.session import get_db

router = APIRouter()

@router.get("/")
def read_attorneys(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    attorneys = db.query(Attorney).offset(skip).limit(limit).all()
    return attorneys