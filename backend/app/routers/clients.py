from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.database import get_db
from app.schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse, ClientWithVisitsResponse
from app.models.dim_client import DimClient
from app.models.fact_visits_payments import FactVisitsPayments
from app.services.client_service import (
    get_all_clients,
    get_client_by_id,
    create_client,
    update_client,
    delete_client
)

router = APIRouter(
    tags=["Clients"]
)

@router.get("/search", response_model=List[ClientResponse])
def search_client(full_name: str, db: Session = Depends(get_db)):
    clients = db.query(DimClient).filter(DimClient.full_name.ilike(f"%{full_name}%")).all()
    return clients

@router.get("/", response_model=List[ClientResponse])
def read_clients(db: Session = Depends(get_db)):
    return get_all_clients(db)


@router.get("/{client_id}", response_model=ClientResponse)
def read_client(client_id: int, db: Session = Depends(get_db)):
    client = get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.get("/with-visits", response_model=List[ClientWithVisitsResponse])
def get_clients_with_visits(db: Session = Depends(get_db)):
    results = (
        db.query(
            DimClient.client_id,
            DimClient.full_name,
            DimClient.age,
            DimClient.phone,
            DimClient.email,
            func.coalesce(func.sum(FactVisitsPayments.visit_count), 0).label("visit_count")
        )
        .outerjoin(FactVisitsPayments, DimClient.client_id == FactVisitsPayments.client_id)
        .group_by(
            DimClient.client_id,
            DimClient.full_name,
            DimClient.age,
            DimClient.phone,
            DimClient.email
        )
        .all()
    )

    return [
        {
            "client_id": r.client_id,
            "full_name": r.full_name,
            "age": r.age,
            "phone": r.phone,
            "email": r.email,
            "visit_count": r.visit_count
        }
        for r in results
    ]


@router.post("/", response_model=ClientResponse)
def create_new_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)


@router.put("/{client_id}", response_model=ClientResponse)
def update_existing_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    return update_client(db, client_id, client)


@router.delete("/{client_id}")
def delete_existing_client(client_id: int, db: Session = Depends(get_db)):
    return delete_client(db, client_id)


