from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import clients, trainers, memberships, classes, dates, visits, notifications, reports

  


app = FastAPI(title="Fitness Club API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reports, prefix="/api/reports")
app.include_router(notifications, prefix="/api/notifications")
app.include_router(clients, prefix="/api/clients")
app.include_router(trainers, prefix="/api/trainers")
app.include_router(memberships, prefix="/api/memberships")
app.include_router(classes, prefix="/api/classes")
app.include_router(dates, prefix="/api/dates")
app.include_router(visits, prefix="/api/visits")


@app.get("/")
def root():
    return {"message": "Fitness Club API is running"}