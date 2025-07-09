from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from models.calendar_day import CalendarDay
from typing import Optional
from schemas.calendar_day import CalendarDayInDB

logger = setup_logger("repositories.calendar_day")

class CalendarDayRepository:
    """
    ### Репозиторий CRUD-логики календарных дней
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        ### Создаёт экземпляр для работы с асинхронной сессией БД
        """

        self._session = session

    async def create_day(self, day_data: CalendarDay) -> Optional[CalendarDayInDB]:
        """
        ### Создаёт календарный день
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: {day_data}")
            self._session.add(day_data)
            await self._session.commit()
            await self._session.refresh(day_data)
            logger.info(f"Календарный день успешно создан (перед валидацией): {day_data}")
            return CalendarDayInDB.model_validate(day_data) if day_data else None
        except Exception as e:
            logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
            await self._session.rollback()
            raise