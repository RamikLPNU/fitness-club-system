from sqlalchemy import Column, Integer, Date, String
from app.database import Base

class DimDate(Base):
    __tablename__ = "dim_date"

    date_id = Column(Integer, primary_key=True)
    full_date = Column(Date)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    weekday = Column(String(20))
    
    @property
    def id(self):
        return self.date_id

# Backwards-compatible export used by service layer
Date = DimDate
