from fastapi import FastAPI

from app.core.config import settings

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }