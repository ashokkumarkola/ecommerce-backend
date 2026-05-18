from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings

# CREATE ASYNC ENGINE 
engine = create_async_engine(
    url=str(settings.DATABASE_URL),

    echo=settings.DATABASE_ECHO,

    # pool_size=settings.DATABASE_POOL_SIZE,
    # max_overflow=settings.DATABASE_MAX_OVERFLOW,
    # pool_timeout=settings.DATABASE_POOL_TIMEOUT,
    # pool_recycle=settings.DATABASE_POOL_RECYCLE,
    # pool_pre_ping=settings.DATABASE_POOL_PRE_PING,

    # future=True,
)

async def check_db_connection():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))