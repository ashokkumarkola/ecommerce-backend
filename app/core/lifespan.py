from contextlib import asynccontextmanager

from fastapi import FastAPI

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