from sqlalchemy import Column, Integer, String
from app.database import Base

class DimTrainer(Base):
    __tablename__ = "dim_trainer"

    trainer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    age = Column(Integer)
    specialization = Column(String(255))
    phone = Column(String(20))

# Backwards-compatible export used by service layer
Trainer = DimTrainer
