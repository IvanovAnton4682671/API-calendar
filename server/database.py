from core.logger import setup_logger
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings
from typing import AsyncGenerator

logger = setup_logger("database")

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
    """Возвращает асинхронную сессию для работы с PostgreSQL

    Асинхронно создаёт и возвращает сессию для работы с БД PostgreSQL

    Returns:
        AsyncGenerator[AsyncSession, None]: Асинхронная сессия, работа с которой
            происходит с использованием асинхронного контекстного менеджера

    Raises:
        Exception: В непредвиденной ситуации

    Examples:
        >>>async with get_db_connection() as session:
        >>>result = await session.execute("SELECT * FROM db_name;")
        >>>print(result.scalars().all())
    """

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            desc = f"При работе с асинхронной сессией произошла ошибка: {str(e)}"
            logger.critical(desc, exc_info=True)
            await session.rollback()
            raise e
        finally:
            await session.close()