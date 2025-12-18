from pydantic import BaseModel
from datetime import date
from typing import Optional


class ClientBase(BaseModel):
    full_name: str
    age: int
    phone: str
    email: str      

class ClientWithVisitsResponse(BaseModel):
    full_name: str
    age: int
    phone: str
    email: str
    visit_count: int

    class Config:
        from_attributes = True

class ClientCreate(ClientBase):
    full_name: str
    age: int
    phone: str
    email: str
    registration_date: Optional[date] = None        

class ClientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class ClientResponse(ClientBase):
    client_id: int
    registration_date: date

    class Config:
        from_attributes = True
