from sqlalchemy.orm import Session
from sqlalchemy import func
import matplotlib.pyplot as plt
from app.database import SessionLocal
from app.models import DimClient, DimTrainer, DimClass, FactVisitsPayments
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

# Repository

class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_clients_with_activity(self):
        results = (
            self.db.query(DimClient.full_name, func.count(FactVisitsPayments.fact_id).label("visits"))
            .join(FactVisitsPayments, DimClient.client_id == FactVisitsPayments.client_id)
            .group_by(DimClient.client_id)
            .all()
        )
        return [{"client": r[0], "visits": r[1]} for r in results]


# Strategy 

class LoadStrategy(ABC):
    @abstractmethod
    def calculate(self, db: Session):
        pass

class DailyLoadStrategy(LoadStrategy):
    def __init__(self, target_date):
        self.target_date = target_date

    def calculate(self, db: Session):
        results = (
            db.query(DimTrainer.full_name, DimClass.hall_name, func.count(FactVisitsPayments.fact_id).label("sessions"))
            .join(FactVisitsPayments, DimTrainer.trainer_id == FactVisitsPayments.trainer_id)
            .join(DimClass, DimClass.class_id == FactVisitsPayments.class_id)
            .filter(FactVisitsPayments.date_id == self.target_date)
            .group_by(DimTrainer.trainer_id, DimClass.class_id)
            .all()
        )
        return [{"trainer": r[0], "hall": r[1], "sessions": r[2]} for r in results]

class TrainerLoadContext:
    def __init__(self, strategy: LoadStrategy):
        self.strategy = strategy

    def execute(self, db: Session):
        return self.strategy.calculate(db)


# Звіт по доходах

def income_report(db: Session, year: int, month: int = None):
    query = db.query(
        func.SUM(FactVisitsPayments.payment_amount).label("income"),
        func.MONTH(FactVisitsPayments.date_id).label("month")
    )
    query = query.filter(func.YEAR(FactVisitsPayments.date_id) == year)
    if month:
        query = query.filter(func.MONTH(FactVisitsPayments.date_id) == month)
    query = query.group_by(func.MONTH(FactVisitsPayments.date_id)).order_by(func.MONTH(FactVisitsPayments.date_id))
    results = query.all()
    return [{"month": r[1], "income": float(r[0] or 0)} for r in results]


# 1

def plot_client_list(clients):
    names = [c["client"] for c in clients]
    visits = [c["visits"] for c in clients]

    plt.figure(figsize=(6, len(clients)*0.6))
    bars = plt.barh(names, visits, color="skyblue")
    plt.xlabel("Кількість відвідувань")
    plt.title("Активність клієнтів (список)")

    for bar, count in zip(bars, visits):
        plt.text(count + 0.1, bar.get_y() + bar.get_height()/2, str(count), va='center')

    plt.tight_layout()
    plt.savefig("client_activity_list.png")
    plt.show()


# 2

def plot_income_report(data):
    months = [d["month"] for d in data]
    incomes = [d["income"] for d in data]

    plt.figure(figsize=(8,5))
    plt.plot(months, incomes, marker="o", color="green")
    plt.title("Доходи клубу")
    plt.ylabel("Доходи (грн)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("income_report.png")
    plt.show()


# 3

def plot_trainer_month_load(db: Session):
    year = int(input("Введіть рік: "))
    month = int(input("Введіть місяць (1-12): "))


    results = (
        db.query(
            DimTrainer.full_name,
            func.count(FactVisitsPayments.fact_id).label("sessions")
        )
        .join(FactVisitsPayments, DimTrainer.trainer_id == FactVisitsPayments.trainer_id)
        .filter(func.YEAR(FactVisitsPayments.date_id) == year)
        .filter(func.MONTH(FactVisitsPayments.date_id) == month)
        .group_by(DimTrainer.trainer_id)
        .all()
    )

    trainers = [r[0] for r in results]
    sessions = [r[1] for r in results]

    plt.figure(figsize=(10,6))
    bars = plt.bar(trainers, sessions, color="skyblue")
    plt.title(f"Завантаженість тренерів за {month}/{year}")
    plt.ylabel("Кількість занять")
    plt.xticks(rotation=45, ha="right")
    for bar, count in zip(bars, sessions):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(count), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig("trainer_month_load.png")
    plt.show()


def plot_hall_month_load(db: Session):
    year = int(input("Введіть рік: "))
    month = int(input("Введіть місяць (1-12): "))


    results = (
        db.query(
            DimClass.hall_name,
            func.count(FactVisitsPayments.fact_id).label("sessions")
        )
        .join(FactVisitsPayments, DimClass.class_id == FactVisitsPayments.class_id)
        .filter(func.YEAR(FactVisitsPayments.date_id) == year)
        .filter(func.MONTH(FactVisitsPayments.date_id) == month)
        .group_by(DimClass.class_id)
        .all()
    )

    halls = [r[0] for r in results]
    sessions = [r[1] for r in results]

    plt.figure(figsize=(10,6))
    bars = plt.bar(halls, sessions, color="lightgreen")
    plt.title(f"Завантаженість залів за {month}/{year}")
    plt.ylabel("Кількість занять")
    plt.xticks(rotation=45, ha="right")
    for bar, count in zip(bars, sessions):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(count), ha='center', va='bottom')
    plt.tight_layout()
    plt.savefig("hall_month_load.png")
    plt.show()
    

if __name__ == "__main__":
    db = SessionLocal()


    repo = ClientRepository(db)
    clients = repo.get_all_clients_with_activity()
    plot_client_list(clients)


    year_input = int(input("Введіть рік для доходів: "))
    month_input_str = input("Введіть місяць (1-12) або залиште порожнім для всього року: ")
    month_input = int(month_input_str) if month_input_str.strip() else None
    income_data = income_report(db, year=year_input, month=month_input)
    plot_income_report(income_data)


    plot_trainer_month_load(db)
    plot_hall_month_load(db)