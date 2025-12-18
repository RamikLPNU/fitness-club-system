from sqlalchemy import Column, Integer, String
from app.database import Base

class DimClass(Base):
    __tablename__ = "dim_class"

    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_name = Column(String(255), nullable=False)
    class_type = Column(String(50))
    hall_name = Column(String(255))
