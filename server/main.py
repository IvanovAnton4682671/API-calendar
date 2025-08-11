from core.logger import setup_logger
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
import router
import uvicorn
from core.config import settings

logger = setup_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Создание таблицы БД

    Создаёт таблицу БД при старте сервиса
    Предполагается использование только при старте сервера

    Args:
        app (FastAPI): Экземпляр сервера

    Raises:
        HTTPException: В непредвиденной ситуации
    """

    try:
        logger.info("Создание таблицы")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблица создана")
    except Exception as e:
        desc = f"При создании таблицы произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )
    yield
    logger.info("Остановка сервера")
    await engine.dispose()

app = FastAPI(
    title="Calendar-API",
    description="API-сервис производственного календаря",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ADMIN_PANEL_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router.router)

@app.get("/")
async def root() -> dict:
    """Заглушка

    Обычная заглушка, показывает что сервер запущен
    Предполагается использование только в роутинге

    Returns:
        dict: Словарь с информацией о запуске сервера
    """
    return {"message": "Calendar-API is running..."}

if __name__ == "__main__":
    logger.info("API-сервис производственного календаря запущен")
    uvicorn.run(
        settings.APP_NAME,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG
    )