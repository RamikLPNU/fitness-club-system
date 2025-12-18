from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.date_schema import DateCreate, DateResponse
from app.services.date_service import get_all_dates, create_date

router = APIRouter(
    tags=["Dates"]
)


@router.get("/", response_model=List[DateResponse])
def read_dates(db: Session = Depends(get_db)):
    return get_all_dates(db)


@router.post("/", response_model=DateResponse)
def create_new_date(data: DateCreate, db: Session = Depends(get_db)):
    return create_date(db, data)
