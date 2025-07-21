from core.logger import setup_logger
from security import verify_auth
from fastapi import APIRouter, Query, Depends
from schemas import CalendarDayInDB, CalendarDayInput
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_connection
from typing import Optional, Union
from services.calendar_day import CalendarDayService
from datetime import date
from services.external import ExternalService

logger = setup_logger("router")

router = APIRouter(tags=["Calendar day"])

@router.post("/date", dependencies=[Depends(verify_auth)], response_model=CalendarDayInDB)
async def create_day(
    day_data: CalendarDayInput,
    note: Optional[str] = Query(None, description="Дополнительное описание дня"),
    session: AsyncSession = Depends(get_db_connection)
) -> CalendarDayInDB:
    """Создаёт календарный день

    Создаёт календарный день по полученным данным
    Предполагается использование только в роутинге

    Args:
        day_data (CalendarDayInput): Данные для создания дня
        note (Optional[str]): Опциональное описание дня
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Returns:
        CalendarDayInDB: Представление созданного дня в БД
    """

    logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
    day_service = CalendarDayService(session)
    created_day = await day_service.create_day(day_data, note)
    logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
    return created_day

@router.get("/period/{period}", response_model=dict)
async def get_days_by_period(
    period: str,
    compact: Optional[bool] = Query(False, description="Флаг сокращённого формата вывода"),
    week_type: Optional[int] = Query(5, ge=5, le=6, description="Тип рабочей недели"),
    statistic: Optional[bool] = Query(False, description="Подробная статистика по выбранному периоду"),
    session: AsyncSession = Depends(get_db_connection)
) -> dict:
    """Получает календарные дни по периоду

    Получает календарные дни по периоду period, а также форматирует вид списка в зависимости
    от параметров compact, week_type и statistic
    Предполагается использование только в роутинге

    Args:
        period (str): Временной период получаемых дней
        compact (Optional[bool]): Статус формата вывода данных (True - сокращённый, False - полный)
        week_type (Optional[int]): Формат рабочей недели (5- или 6-дневная)
        statistic (Optional[bool]): Статус статистики (True - полная, False - сокращённая)
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Returns:
        dict: Словарь со всей информацией
    """

    logger.info(f"Пробуем получить календарные дни по периоду={period}")
    day_service = CalendarDayService(session)
    result = await day_service.get_days_by_period(period, compact, week_type, statistic)
    logger.info(f"Календарные дни по периоду={period} успешно получены")
    return result

@router.put("/date/{date}", dependencies=[Depends(verify_auth)], response_model=Union[CalendarDayInDB, dict])
async def update_day(
    date: date,
    day_data: CalendarDayInput,
    note: Optional[str] = Query(None, description="Дополнительное описание дня"),
    session: AsyncSession = Depends(get_db_connection)
) -> Union[CalendarDayInDB, dict]:
    """Обновляет календарный день по дате

    Обновляет календарный день по дате date данными day_data и note
    Предполагается использование только в роутинге

    Args:
        date (date): Дата обновляемого дня
        day_data (CalendarDayInput): Данные для обновления дня
        note (Optional[str]): Опциональное описание дня
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Returns:
        Union[CalendarDayInDB, dict]: Возвращает либо обновлённый день, либо пустой словарь (если день не существует)
    """

    logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
    day_service = CalendarDayService(session)
    updated_day = await day_service.update_day(date, day_data, note)
    if updated_day:
        logger.info(f"Календарный день date={date} успешно обновлён (после валидации): {updated_day}")
        return updated_day
    else:
        logger.warning(f"Календарный день date={date} не существует")
        return {"message": f"Календарный день date={date} не существует"}

@router.delete("/date/{date}", dependencies=[Depends(verify_auth)], response_model=dict)
async def delete_day(date: date, session: AsyncSession = Depends(get_db_connection)) -> dict:
    """Удаляет календарный день по дате

    Удаляет календарный день по дате date
    Предполагается использование только в роутинге

    Args:
        date (date): Дата удаляемого дня
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Returns:
        dict: Словарь со статусом удаления дня
    """

    logger.info(f"Пробуем удалить календарный день date={date}")
    day_service = CalendarDayService(session)
    deleted_status = await day_service.delete_day(date)
    if deleted_status:
        logger.info(f"Календарный день date={date} успешно удалён")
        return {"message": f"Календарный день date={date} успешно удалён"}
    else:
        logger.warning(f"Календарный день date={date} не существует")
        return {"message": f"Календарный день date={date} не существует"}

@router.get("/external/period/{year}", response_model=dict)
async def get_days_by_year(
    year: int,
    week_type: int = Query(5, ge=5, le=6, description="Тип рабочей недели"),
    statistic: bool = Query(False, description="Подробная статистика по выбранному периоду")
) -> dict:
    """Получает календарные дни за год

    Запрашивает HTML-страницу календаря, затем парсит её,  формирует и форматирует итоговый список дней,
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