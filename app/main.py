from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.db.database import Base, engine
from app.db import models

from fastapi.staticfiles import StaticFiles


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Document Manager",
    description="Document management system for managers",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def root():
    return {
        "message": "AI Document Manager API is running"
    }


app.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"],
)