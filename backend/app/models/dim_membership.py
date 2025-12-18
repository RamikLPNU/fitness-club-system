from sqlalchemy import Column, Integer, String, DECIMAL
from app.database import Base

class DimMembership(Base):
    __tablename__ = "dim_membership"

    membership_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100))
    duration_days = Column(Integer)
    price = Column(DECIMAL(10, 2))
