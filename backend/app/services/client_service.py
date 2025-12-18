from sqlalchemy.orm import Session
from app.models.dim_client import DimClient
from app.schemas.client_schema import ClientCreate, ClientUpdate
from datetime import date


def get_all_clients(db: Session):
    return db.query(DimClient).all()


def get_client_by_id(db: Session, client_id: int):
    return db.query(DimClient).filter(DimClient.client_id == client_id).first()


def create_client(db: Session, client: ClientCreate):
    new_client = DimClient(
        full_name=client.full_name,
        age=client.age,
        phone=client.phone,
        email=client.email,
        registration_date=client.registration_date or date.today()
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


def update_client(db: Session, client_id: int, client: ClientUpdate):
    db_client = get_client_by_id(db, client_id)

    for key, value in client.dict(exclude_unset=True).items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


def delete_client(db: Session, client_id: int):
    db_client = get_client_by_id(db, client_id)

    if not db_client:
        return {"error": "Client not found"}

    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted successfully"}
