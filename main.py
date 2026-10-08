from fastapi import FastAPI

from app.database import engine, Base
from app import models
from app.routes.jobs import router as jobs_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bulk Certificate Generator",
    description="API for generating certificates in bulk",
    version="1.0.0"
)


# Include Jobs API
app.include_router(jobs_router)


@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }