from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.core.config import settings
from app.core.database import check_db_connection
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logger.info("Starting application...")

    await check_db_connection()
    logger.info("Database connected")
    
    yield

    # SHUTDOWN
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern e-commerce backend built with FastAPI",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }