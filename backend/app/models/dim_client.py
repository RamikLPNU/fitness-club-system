from datetime import date
from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class DimClient(Base):
    __tablename__ = "dim_client"

    client_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    age = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100))
    registration_date = Column(Date, nullable=False, default=date.today)    
