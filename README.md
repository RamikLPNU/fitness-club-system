# Fitness Club Management System

Інформаційна система для автоматизації роботи фітнес-клубу.
Проєкт реалізований в рамках курсової роботи з дисципліни
"Software Engineering and Design".

---

Запуск проєкту

Клонування репозиторію

git clone https://github.com/RamikLPNU/fitness-club-system

cd fitness-club-system

Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Створити базу даних MySQL

CREATE DATABASE fitness_club;

У файлі database.py вказати параметри підключення:

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost/fitness_club"

Запуск сервера

uvicorn app.main:app --reload

Сервер доступний за адресою:
http://localhost:8000

Документація API:
http://localhost:8000/docs

Frontend

Відкрити файл frontend/index.html у браузері.
