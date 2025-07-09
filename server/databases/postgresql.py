from core.logger import setup_logger
from sqlalchemy.orm import declarative_base
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

logger = setup_logger("databases.postgresql")

Base = declarative_base()

engine = create_async_engine(
    settings.POSTGRESQL_URL.get_secret_value(),
    echo=True,
    future=True,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=True,
    expire_on_commit=False
)

async def get_db_connection() -> AsyncGenerator[AsyncSession, None]:
    """
    ### Асинхронно создаёт и возвращает сессию для работы с БД PostgreSQL
    """

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.critical(f"При работе с асинхронной сессией произошла ошибка: {str(e)}", exc_info=True)
            await session.rollback()
            raise
        finally:
            await session.close()