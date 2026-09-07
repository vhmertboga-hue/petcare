import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.app.models import Business
from backend.app.db.session import Base


async def _create_tables():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


def test_business_model_import():
    # sanity check: Business class is importable
    assert hasattr(Business, "__tablename__")
