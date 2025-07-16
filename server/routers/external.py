from core.logger import setup_logger
from fastapi import APIRouter, Query
from services.external import ExternalService

logger = setup_logger("routers.external")

router = APIRouter(
    prefix="/external",
    tags=["isDayOff"]
)

@router.get("/period/{year}", response_model=dict)
async def get_days_by_year(
    year: int,
    week_type: int = Query(5, ge=5, le=6, description="Тип рабочей недели"),
    statistic: bool = Query(False, description="Подробная статистика по выбранному периоду")
) -> dict:
    """Получает календарные дни за год

    Получает календарные дни за определённый год, затем формирует и форматирует итоговый список дней,
    зависящий от параметров week_type и statistic
    Предполагается использование только в роутинге

    Args:
        year (int): Год, за который получает список дней
        week_type (int): Тип рабочей недели
        statistic (bool): Формат формируемой статистики

    Returns:
        dict: Словарь со всей информацией
    """

    logger.info(f"Пробуем получить календарные дни по параметрам: год={year}, рабочая неделя={week_type}")
    external_service = ExternalService()
    result = await external_service.get_days_by_year(year, week_type, statistic)
    logger.info(f"Календарные дни (год={year}, рабочая неделя={week_type}) успешно получены")
    return result