from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from models.calendar_day import CalendarDay
from typing import Optional
from schemas.calendar_day import CalendarDayInDB
import datetime
from sqlalchemy import select, update

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
            if day_data:
                logger.info(f"Календарный день успешно создан (перед валидацией): {day_data}")
                return CalendarDayInDB.model_validate(day_data)
            logger.warning("При создании календарного дня что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
            await self._session.rollback()
            raise

    async def get_day_by_date(self, date: datetime.date) -> Optional[CalendarDay]:
        """
        ### Ищет календарный день по date
        """

        try:
            logger.info(f"Пробуем получить день по date={date}")
            query = select(CalendarDay).where(CalendarDay.date == date)
            result = await self._session.execute(query)
            received_day = result.scalars().first()
            if received_day:
                logger.info(f"Календарный день успешно получен: {received_day}")
                return received_day
            logger.warning("При получении дня что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При получении календарного дня произошла ошибка: {str(e)}", exc_info=True)
            raise

    async def update_day(self, date: datetime.date, day_data: CalendarDay) -> Optional[CalendarDayInDB]:
        """
        ### Обновляет календарный день, полученный по date
        """

        try:
            logger.info(f"Пробуем обновить день date={date} данными: {day_data}")
            received_day = await self.get_day_by_date(date)
            if received_day:
                received_day.date = day_data.date
                received_day.type_id = day_data.type_id
                received_day.type_text = day_data.type_text
                received_day.note = day_data.note
                received_day.week_day = day_data.week_day
                await self._session.commit()
                await self._session.refresh(received_day)
                if received_day:
                    logger.info(f"Календарный день date={date} успешно обновлён (перед валидацией): {received_day}")
                    return CalendarDayInDB.model_validate(received_day)
                logger.warning(f"При обновлении данных дня date={date} что-то пошло не так")
                return None
            logger.warning(f"День date={date} не существует")
            return None
        except Exception as e:
            logger.error(f"При обновлении календарного дня произошла ошибка: {str(e)}", exc_info=True)
            await self._session.rollback()
            raise