from sqlalchemy.orm import Session
from . import models
from .schemas import client_schema, trainer_schema, membership_schema, visit_schema, date_schema

# ======================
# Clients
# ======================
def get_clients(db: Session):
    return db.query(models.DimClient).all()

def get_client(db: Session, client_id: int):
    return db.query(models.DimClient).filter(models.DimClient.client_id == client_id).first()

def create_client(db: Session, client: client_schema.ClientCreate):
    db_client = models.DimClient(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# ======================
# Trainers
# ======================
def get_trainers(db: Session):
    return db.query(models.DimTrainer).all()

def create_trainer(db: Session, trainer: trainer_schema.TrainerCreate):
    db_trainer = models.DimTrainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

# ======================
# Memberships
# ======================
def get_memberships(db: Session):
    return db.query(models.DimMembership).all()

def create_membership(db: Session, membership: membership_schema.MembershipCreate):
    db_m = models.DimMembership(**membership.dict())
    db.add(db_m)
    db.commit()
    db.refresh(db_m)
    return db_m

# ======================
# Visits / Payments
# ======================
def create_visit_payment(db: Session, vp: visit_schema.VisitPaymentCreate):
    db_v = models.FactVisitsPayments(**vp.dict())
    db.add(db_v)
    db.commit()
    db.refresh(db_v)
    return db_v

def get_visits(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FactVisitsPayments).offset(skip).limit(limit).all()

# ======================
# Reports / Analytics
# ======================
def get_income_by_month(db: Session):
    from sqlalchemy import func
    q = (
        db.query(
            models.DimDate.year,
            models.DimDate.month,
            func.sum(models.FactVisitsPayments.payment_amount).label("income")
        )
        .join(
            models.FactVisitsPayments,
            models.DimDate.date_id == models.FactVisitsPayments.date_id
        )
        .group_by(models.DimDate.year, models.DimDate.month)
        .order_by(models.DimDate.year, models.DimDate.month)
    )
    return q.all()
