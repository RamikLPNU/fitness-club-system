from sqlalchemy.orm import Session
from app.models.dim_trainer import Trainer
from app.schemas.trainer_schema import TrainerCreate, TrainerUpdate


def get_all_trainers(db: Session):
    return db.query(Trainer).all()


def create_trainer(db: Session, trainer: TrainerCreate):
    db_trainer = Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer


def update_trainer(db: Session, trainer_id: int, trainer: TrainerUpdate):
    db_trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()

    for key, value in trainer.dict(exclude_unset=True).items():
        setattr(db_trainer, key, value)

    db.commit()
    db.refresh(db_trainer)
    return db_trainer
