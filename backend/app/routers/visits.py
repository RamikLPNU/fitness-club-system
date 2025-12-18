from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.visit_schema import VisitCreate, VisitResponse
from app.services.visit_payment_service import (
    create_visit_payment,
    get_all_visits_payments
)

router = APIRouter(
    tags=["Visits & Payments"]
)


@router.get("/", response_model=List[VisitResponse])
def read_visits(db: Session = Depends(get_db)):
    return get_all_visits_payments(db)


@router.post("/", response_model=VisitResponse)
def create_visit(data: VisitCreate, db: Session = Depends(get_db)):
    return create_visit_payment(db, data)

