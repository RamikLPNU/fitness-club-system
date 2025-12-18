from pydantic import BaseModel
from datetime import date
from typing import Optional


class MembershipBase(BaseModel):
    price: int
    name: str
    duration_days: int
    


class MembershipCreate(MembershipBase):
    pass


class MembershipUpdate(BaseModel):
    name: Optional[str] = None
    duration_days: Optional[int] = None
    price: Optional[int] = None


class MembershipResponse(MembershipBase):
    membership_id: int

    class Config:
        from_attributes = True
