from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models.dim_client import DimClient
from app.models.fact_visits_payments import FactVisitsPayments
from app.models.dim_membership import DimMembership
from app.models.dim_trainer import DimTrainer
from app.models.dim_class import DimClass

router = APIRouter(
    tags=["Reports"]
)

# 1. Активність клієнтів
@router.get("/client-activity")
def client_activity(db: Session = Depends(get_db)):
    results = (
        db.query(DimClient.full_name, func.count(FactVisitsPayments.fact_id).label("visits"))
        .join(FactVisitsPayments, DimClient.client_id == FactVisitsPayments.client_id)
        .group_by(DimClient.client_id)
        .all()
    )
    return [{"client": r[0], "visits": r[1]} for r in results]


# 2. Доходи клубу по місяцях
@router.get("/income")
def income(year: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            func.MONTH(DimClient.registration_date).label("month"),
            func.SUM(FactVisitsPayments.payment_amount).label("income")
        )
        .join(FactVisitsPayments, DimClient.client_id == FactVisitsPayments.client_id)
        .filter(func.YEAR(DimClient.registration_date) == year)
        .group_by("month")
        .order_by("month")
        .all()
    )

    month_names = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }

    return [{"month": month_names.get(r[0], str(r[0])), "income": float(r[1] or 0)} for r in results]

# 3. Завантаженість тренерів та залів
@router.get("/trainer-load")
def trainer_load(db: Session = Depends(get_db)):
    results = (
        db.query(DimTrainer.full_name, DimClass.hall_name, func.count(FactVisitsPayments.fact_id).label("sessions"))
        .join(FactVisitsPayments, DimTrainer.trainer_id == FactVisitsPayments.trainer_id)
        .join(DimClass, DimClass.class_id == FactVisitsPayments.class_id)
        .group_by(DimTrainer.trainer_id, DimClass.class_id)
        .all()
    )
    return [{"trainer": r[0], "hall": r[1], "sessions": r[2]} for r in results]
