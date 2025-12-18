from sqlalchemy.orm import Session
from app.models.dim_membership import DimMembership
from app.schemas.membership_schema import MembershipCreate, MembershipUpdate


def get_all_memberships(db: Session):
    return db.query(DimMembership).all()


def create_membership(db: Session, membership: MembershipCreate):
    db_membership = DimMembership(**membership.dict())
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership


def update_membership(db: Session, membership_id: int, membership: MembershipUpdate):
    db_membership = db.query(DimMembership).filter(DimMembership.id == membership_id).first()

    for key, value in membership.dict(exclude_unset=True).items():
        setattr(db_membership, key, value)

    db.commit()
    db.refresh(db_membership)
    return db_membership
