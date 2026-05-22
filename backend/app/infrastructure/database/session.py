"""
Database Session - Connection pool and session management
"""

import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings
from app.infrastructure.database.bootstrap import seed_microsegments_if_empty
from app.infrastructure.database.models import Base

logger = logging.getLogger(__name__)
settings = get_settings()

engine = None
SessionLocal = None


def _get_engine():
    global engine
    if engine is None:
        engine_kwargs = {
            "echo": settings.DATABASE_ECHO,
            "pool_pre_ping": True,
        }
        if settings.ENVIRONMENT == "test":
            engine_kwargs["poolclass"] = NullPool
        else:
            engine_kwargs["pool_size"] = settings.DATABASE_POOL_SIZE
            engine_kwargs["max_overflow"] = settings.DATABASE_MAX_OVERFLOW
            engine_kwargs["pool_recycle"] = settings.DATABASE_POOL_RECYCLE

        engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)
    return engine


def _get_session_factory():
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = async_sessionmaker(
            _get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return SessionLocal


async def get_session() -> AsyncSession:
    """Get database session"""
    session_factory = _get_session_factory()
    async with session_factory() as session:
        yield session


async def init_db():
    """Initialize database - create tables"""
    try:
        active_engine = _get_engine()
        async with active_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await seed_microsegments_if_empty(_get_session_factory())
        logger.info("Database tables created successfully")
    except Exception as exc:
        logger.error(f"Failed to initialize database: {exc}")
        raise


async def close_db():
    """Close database connection"""
    if engine is not None:
        await engine.dispose()
        logger.info("Database connection closed")
