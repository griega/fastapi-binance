from core.logs import log
import traceback
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import settings

DB_URL = f"postgresql+asyncpg://{settings.pg_user}:{settings.pg_password}@{settings.pg_host}:{settings.pg_port}/{settings.db_name}"
engine = create_async_engine(
    DB_URL, pool_pre_ping=True, echo=False, pool_size=10, max_overflow=10
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    """Get async db Session"""
    db = AsyncSessionLocal()
    try:
        yield db
        await db.commit()
    except Exception as ex_db:
        log.error(ex_db)
        await db.rollback()
        log.error(traceback.format_exc())
    finally:
        await db.close()