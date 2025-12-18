from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from app.database import get_db
from app.models.dim_client import DimClient
from app.models.dim_membership import DimMembership
from app.models.fact_visits_payments import FactVisitsPayments

router = APIRouter(
    tags=["Notifications"]
)

@router.get("/expiring-memberships")
def expiring_memberships(db: Session = Depends(get_db)):
    today = date.today()
    result = []

    records = (
        db.query(DimClient, DimMembership)
        .join(FactVisitsPayments, DimClient.client_id == FactVisitsPayments.client_id)
        .join(DimMembership, FactVisitsPayments.membership_id == DimMembership.membership_id)
        .all()
    )

    for client, membership in records:
        expiry_date = client.registration_date + timedelta(days=membership.duration_days)
        days_left = (expiry_date - today).days

        if days_left <= 7:
            result.append({
                "client_name": client.full_name,
                "phone": client.phone,
                "membership": membership.name,
                "days_left": days_left,
                "status": "Expired" if days_left < 0 else "Expiring soon"
            })

    return result
    