from fastapi import APIRouter, Depends, HTTPException           
from app.schemas import trainer_schema
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db
from app.models.dim_trainer import DimTrainer
from app.models.dim_client import DimClient
from app.models.fact_visits_payments import FactVisitsPayments
from app.schemas.class_schema import  ClassResponse
from app.services.trainer_schedule import DEFAULT_TRAINER_SCHEDULE

router = APIRouter(
    tags=["Trainers"]
)

DEFAULT_TRAINER_SCHEDULE = [
    {"weekday": "Понеділок", "start_time": "09:00", "end_time": "17:00"},
    {"weekday": "Вівторок", "start_time": "09:00", "end_time": "17:00"},
    {"weekday": "Середа", "start_time": "09:00", "end_time": "17:00"},
    {"weekday": "Четвер", "start_time": "09:00", "end_time": "17:00"},
    {"weekday": "Пʼятниця", "start_time": "09:00", "end_time": "17:00"},
]

@router.get('/', response_model=list[trainer_schema.TrainerResponse])
def list_trainers(db: Session = Depends(get_db)):
    return crud.get_trainers(db)

@router.post('/', response_model=trainer_schema.TrainerResponse)
def create_trainer(trainer: trainer_schema.TrainerCreate, db: Session = Depends(get_db)):
    return crud.create_trainer(db, trainer)

@router.get("/{trainer_id}/profile")
@router.get("/{trainer_id}/profile")
def trainer_profile(trainer_id: int, db: Session = Depends(get_db)):
    trainer = db.query(DimTrainer).filter(DimTrainer.trainer_id == trainer_id).first()

    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    return {
        "id": trainer.trainer_id,
        "name": trainer.full_name,
        "specialization": trainer.specialization,
        "phone": trainer.phone,
        "schedule": DEFAULT_TRAINER_SCHEDULE
    }
    
@router.get("/available")
def available_trainers(direction: str, db: Session = Depends(get_db)):
    trainers = (
        db.query(DimTrainer)
        .filter(DimTrainer.specialization == direction)
        .all()
    )
    return trainers
