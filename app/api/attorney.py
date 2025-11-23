from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Attorney

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/attorneys/{jurisdiction}")
def get_attorneys_by_jurisdiction(jurisdiction: str, db: Session = Depends(get_db)):
    attorneys = (
        db.query(Attorney)
        .filter(Attorney.jurisdiction == jurisdiction.upper())
        .all()
    )
    return attorneys

# @router.get("/attorneys")
# def get_attorneys(db: Session = Depends(get_db)):
#     attorneys = (
#         db.query(Attorney).all()
#     )
#     return attorneys