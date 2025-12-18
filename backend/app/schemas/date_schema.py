from pydantic import BaseModel
from datetime import date
from typing import Optional

class DateBase(BaseModel):
    full_date: date
    day: int
    month: int
    year: int
    weekday: str


class DateCreate(BaseModel):
    full_date: date
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    weekday: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2 замість orm_mode


class DateResponse(DateBase):
    id: int

    class Config:
        from_attributes = True
    