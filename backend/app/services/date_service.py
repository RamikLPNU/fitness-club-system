from sqlalchemy.orm import Session
from app.models.dim_date import Date
from app.schemas.date_schema import DateCreate


def get_all_dates(db: Session):
    return db.query(Date).all()


def create_date(db: Session, date: DateCreate):
    new_date = Date(**date.dict())
    db.add(new_date)
    db.commit()
    db.refresh(new_date)
    return new_date
