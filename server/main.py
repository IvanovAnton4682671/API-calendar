from core.logger import setup_logger
from contextlib import asynccontextmanager
from databases.postgresql import engine, Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import calendar_day
import uvicorn
from core.config import settings

logger = setup_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    ### Создание таблиц при старте сервера
    """

    try:
        logger.info("Создание таблицы")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблица создана")
    except Exception as e:
        logger.error(f"При создании таблицы произошла ошибка: {str(e)}", exc_info=True)
        raise
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(calendar_day.router)

@app.get("/")
async def root():
    return {"message": "Calendar-API is running..."}

if __name__ == "__main__":
    logger.info("API-сервис производственного календаря запущен")
    uvicorn.run(
        settings.APP_NAME,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG
    )