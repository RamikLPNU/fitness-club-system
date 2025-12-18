from pydantic import BaseModel
from typing import Optional


class ClassBase(BaseModel):
    class_name: str
    class_type: str
    hall_name: str



class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    class_name: Optional[str] = None
    class_type: Optional[str] = None
    hall_name: Optional[str] = None


class ClassResponse(ClassBase):
    class_id: int

    class Config:
        from_attributes = True
