from core.logger import setup_logger
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from databases.postgresql import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import calendar_day
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
        Exception: В непредвиденной ситуации
    """

    try:
        logger.info("Создание таблицы")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблица создана")
    except Exception as e:
        desc = f"При создании таблицы произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)
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

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Общий обработчик всех ошибок

    Обработчик, который логирует и перехватывает все ошибки

    Args:
        request (Request): Запрос, вызвавший ошибку
        exception (Exception): Какая-то ошибка

    Returns:
        JSONResponse: Ответ обработчика ошибок
    """

    logger.error(f"Запрос: {request.method} {request.url}\nОшибка: {str(exception)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exception)}
    )

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