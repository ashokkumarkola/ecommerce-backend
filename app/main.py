from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.exceptions import register_exception_handlers

from app.modules.users.routes import router as user_router


# APP
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern e-commerce backend built with FastAPI",
    lifespan=lifespan
)

# ROUTES
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }

# EXCEPTION HANDLERS
register_exception_handlers(app)
