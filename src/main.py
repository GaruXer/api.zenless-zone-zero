from fastapi import FastAPI

from src.config import settings
from src.routers import Agent, Bangboo, DriveDisc, WEngine

api_name = "Zenless Zone Zero API"

app = FastAPI(title=api_name, version=settings.API_VERSION)

app.include_router(Agent.router)
app.include_router(Bangboo.router)
app.include_router(DriveDisc.router)
app.include_router(WEngine.router)

@app.get("/")
def read_root():
    return {
        "name": api_name,
        "version": settings.API_VERSION,
        "documentation_url": "/docs"
    }