from sqlalchemy.ext.asyncio import ( 
    create_async_engine, 
    async_sessionmaker, 
    AsyncSession
)

# from app.db.base import Base
from app.core.database import engine
from app.core.config import settings

# ASYNC SESSION FACTORY
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

# ASYNC DATABASE SESSION DEPENDENCY
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
