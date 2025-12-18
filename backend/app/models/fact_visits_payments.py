from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from app.database import Base

class FactVisitsPayments(Base):
    __tablename__ = "fact_visits_payments"

    fact_id = Column(Integer, primary_key=True, autoincrement=True)

    date_id = Column(Integer, ForeignKey("dim_date.date_id"))
    client_id = Column(Integer, ForeignKey("dim_client.client_id"))
    trainer_id = Column(Integer, ForeignKey("dim_trainer.trainer_id"))
    class_id = Column(Integer, ForeignKey("dim_class.class_id"))
    membership_id = Column(Integer, ForeignKey("dim_membership.membership_id"))

    visit_count = Column(Integer)
    payment_amount = Column(DECIMAL(10, 2), default=0.00)
