from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VisitBase(BaseModel):
    client_id: int
    class_id: Optional[int] = None
    date_id: int
    trainer_id: Optional[int] = None
    membership_id: int
    visit_count: int
    payment_amount: int




class VisitCreate(VisitBase):
    pass


class VisitUpdate(BaseModel):
    visit_time: Optional[datetime] = None


class VisitResponse(VisitBase):
    fact_id: int

    class Config:
        from_attributes = True
