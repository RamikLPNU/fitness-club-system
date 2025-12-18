from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.membership_schema import MembershipBase, MembershipCreate, MembershipUpdate
from app.services import membership_service

router = APIRouter(
    tags=["Memberships"]
)

@router.get("/", response_model=list[MembershipBase])
def get_memberships(db: Session = Depends(get_db)):
    return membership_service.get_all_memberships(db)

@router.get("/{membership_id}", response_model=MembershipBase)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = membership_service.get_membership(db, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership

@router.post("/", response_model=MembershipBase)
def create_membership(data: MembershipCreate, db: Session = Depends(get_db)):
    return membership_service.create_membership(db, data)

@router.put("/{membership_id}", response_model=MembershipBase)
def update_membership(membership_id: int, data: MembershipUpdate, db: Session = Depends(get_db)):
    membership = membership_service.update_membership(db, membership_id, data)
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership

@router.delete("/{membership_id}")
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    ok = membership_service.delete_membership(db, membership_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Membership not found")
    return {"message": "Membership deleted"}
