from fastapi import FastAPI

from routers import Agent, Bangboo, DriveDisc, WEngine

app_name = "Zenless Zone Zero API"
version = "0.0.0"

app = FastAPI(title=app_name, version=version)

app.include_router(Agent.router)
app.include_router(Bangboo.router)
app.include_router(DriveDisc.router)
app.include_router(WEngine.router)

@app.get("/")
def read_root():
    return {
        "name": app_name,
        "version": version,
        "documentation_url": "/docs",
    }