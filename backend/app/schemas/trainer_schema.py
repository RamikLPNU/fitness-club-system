from pydantic import BaseModel
from typing import Optional


class TrainerBase(BaseModel):
    full_name: str
    specialization: str
    age: Optional[int] = None
    phone: str


class TrainerCreate(TrainerBase):
    pass


class TrainerUpdate(BaseModel):
    full_name: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None


class TrainerResponse(TrainerBase):
    trainer_id: int

    class Config:
        orm_mode = True
