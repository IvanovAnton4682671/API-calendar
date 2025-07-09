from core.logger import setup_logger
from fastapi import APIRouter, Depends
from schemas.calendar_day import CalendarDayInDB, CalendarDayInput
from sqlalchemy.ext.asyncio import AsyncSession
from databases.postgresql import get_db_connection
from typing import Optional
from services.calendar_day import CalendarDayService

logger = setup_logger("repositories.calendar_day")

router = APIRouter(tags=["Calendar day"])

@router.post("/date", response_model=CalendarDayInDB)
async def create_day(day_data: CalendarDayInput, session: AsyncSession = Depends(get_db_connection)) -> Optional[CalendarDayInDB]:
    """
    ### Создаёт календарный день по полученным данным
    """

    logger.info(f"Пробуем создать день с данными: {day_data}")
    day_service = CalendarDayService(session)
    created_day = await day_service.create_day(day_data)
    logger.info(f"Созданный день: {created_day}")
    return created_day