from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from contextlib import asynccontextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./taskflow.db")

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@asynccontextmanager
async def get_db():
    """Get database session."""
    async with async_session_factory() as session:
        yield session
        await session.close()


async def init_db():
    """Initialize database tables."""
    from src.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connection."""
    await engine.dispose()
