from sqlalchemy.orm import Session
from app.models.dim_class import DimClass
from app.schemas.class_schema import ClassCreate, ClassUpdate


def get_all_classes(db: Session):
    return db.query(DimClass).all()


def create_class(db: Session, class_obj: ClassCreate):
    new_class = DimClass(**class_obj.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


def update_class(db: Session, class_id: int, class_data: ClassUpdate):
    db_class = db.query(DimClass).filter(DimClass.id == class_id).first()

    for key, value in class_data.dict(exclude_unset=True).items():
        setattr(db_class, key, value)

    db.commit()
    db.refresh(db_class)
    return db_class
