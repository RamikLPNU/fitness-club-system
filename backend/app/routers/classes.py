from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.class_schema import ClassCreate, ClassUpdate, ClassResponse
from app.services.class_service import (
    get_all_classes,
    create_class,
    update_class
)

router = APIRouter(
    tags=["Classes"]
)


@router.get("/", response_model=List[ClassResponse])
def read_classes(db: Session = Depends(get_db)):
    return get_all_classes(db)


@router.post("/", response_model=ClassResponse)
def create_new_class(data: ClassCreate, db: Session = Depends(get_db)):
    return create_class(db, data)


@router.put("/{class_id}", response_model=ClassResponse)
def update_existing_class(class_id: int, data: ClassUpdate, db: Session = Depends(get_db)):
    updated = update_class(db, class_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Class not found")
    return updated
