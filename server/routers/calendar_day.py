from core.logger import setup_logger
from fastapi import APIRouter, Query, Depends, HTTPException, status
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
) -> CalendarDayInDB:
    """
    ### Создаёт календарный день
    """

    try:
        logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
        day_service = CalendarDayService(session)
        created_day = await day_service.create_day(day_data, note)
        if created_day:
            logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
            return created_day
        logger.warning(f"При создании календарного дня что-то пошло не так")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка создания календарного дня"
        )
    except Exception as e:
        logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put("/date/{date}", response_model=CalendarDayInDB)
async def update_day(
    date: datetime.date,
    day_data: CalendarDayInput,
    note: Optional[str] = Query(None, description="Дополнительное описание дня"),
    session: AsyncSession = Depends(get_db_connection)
) -> CalendarDayInDB:
    """
    ### Обновляет календарный день по date
    """

    try:
        logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
        day_service = CalendarDayService(session)
        updated_day = await day_service.update_day(date, day_data, note)
        if updated_day:
            logger.info(f"Календарный день date={date} успешно обновлён (после валидации): {updated_day}")
            return updated_day
        logger.warning(f"При обновлении календарного дня date={date} что-то пошло не так")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка обновления календарного дня"
        )
    except Exception as e:
        logger.error(f"При обновлении календарного дня date={date} произошла ошибка: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/date/{date}", response_model=dict)
async def delete_day(date: datetime.date, session: AsyncSession = Depends(get_db_connection)) -> dict:
    """
    ### Удаляет календарный день по date
    """

    try:
        logger.info(f"Пробуем удалить календарный день date={date}")
        day_service = CalendarDayService(session)
        deleted_status = await day_service.delete_day(date)
        if deleted_status:
            logger.info(f"Календарный день date={date} успешно удалён")
            return {"status": True}
        logger.warning(f"При удалении календарного дня date={date} что-то пошло не так")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка удаления календарного дня"
        )
    except Exception as e:
        logger.error(f"При удалении календарного дня date={date} произошла ошибка: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )