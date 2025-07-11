from core.logger import setup_logger
from fastapi import APIRouter, Query, Depends
from schemas.calendar_day import CalendarDayInDB, CalendarDayInput
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgresql import get_db_connection
from typing import Optional
from services.calendar_day import CalendarDayService
import datetime

logger = setup_logger("repositories.calendar_day")

router = APIRouter(tags=["Calendar day"])

@router.post("/date", response_model=CalendarDayInDB)
async def create_day(
    day_data: CalendarDayInput,
    note: Optional[str] = Query(None, description="Дополнительное описание дня"),
    session: AsyncSession = Depends(get_db_connection)
) -> Optional[CalendarDayInDB]:
    """
    ### Создаёт календарный день по полученным данным
    """

    try:
        logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
        day_service = CalendarDayService(session)
        created_day = await day_service.create_day(day_data, note)
        if created_day:
            logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
            return created_day
        logger.warning(f"При создании календарного дня что-то пошло не так")
        return None
    except Exception as e:
        logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
        raise

@router.put("/date/{date}", response_model=CalendarDayInDB)
async def update_day(
    date: datetime.date,
    day_data: CalendarDayInput,
    note: Optional[str] = Query(None, description="Дополнительное описание дня"),
    session: AsyncSession = Depends(get_db_connection)
) -> Optional[CalendarDayInDB]:
    """
    ### Обновляет календарный день, полученный по date
    """

    try:
        logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
        day_service = CalendarDayService(session)
        updated_day = await day_service.update_day(date, day_data, note)
        if updated_day:
            logger.info(f"Календарный день date={date} успешно обновлён (после валидации): {updated_day}")
            return updated_day
        logger.warning("При обновлении календарного дня что-то пошло не так")
        return None
    except Exception as e:
        logger.error(f"При обновлении календарного дня произошла ошибка: {str(e)}", exc_info=True)
        raise