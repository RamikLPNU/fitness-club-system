from sqlalchemy.orm import Session
from app.models.fact_visits_payments import FactVisitsPayments
from app.schemas.visit_schema import VisitCreate


def create_visit_payment(db: Session, visit: VisitCreate):
    new_visit = FactVisitsPayments(**visit.dict())
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit


def get_all_visits_payments(db: Session):
    return db.query(FactVisitsPayments).all()
