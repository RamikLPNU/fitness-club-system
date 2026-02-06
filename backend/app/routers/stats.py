from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.dim_client import DimClient
from app.models.dim_trainer import DimTrainer
from app.models.dim_membership import DimMembership

router = APIRouter(
    tags=["Dashboard Stats"]
)

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    clients_count = db.query(func.count(DimClient.client_id)).scalar()
    trainers_count = db.query(func.count(DimTrainer.trainer_id)).scalar()
    active_memberships = db.query(
            func.count(DimMembership.membership_id)
        ).scalar()
    return {
        "clients": clients_count,
        "trainers": trainers_count,
        "active_memberships": active_memberships
    }
