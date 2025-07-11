from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from core.consts import DAY_TYPES, WEEK_DAYS
from schemas.calendar_day import CalendarDayInput, CalendarDayInDB
from typing import Optional
from models.calendar_day import CalendarDay
import datetime

logger = setup_logger("services.calendar_day")

class CalendarDayService:
    """
    ### Сервис бизнес-логики календарных дней
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        ### Создаёт экземпляр для работы с асинхронной сессией БД
        """

        self._repo = CalendarDayRepository(session)
        self._day_types = DAY_TYPES
        self._week_days = WEEK_DAYS

    def _assemble_day(self, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDay]:
        """
        ### Собирает календарный день `CalendarDay` из его полей
        """

        try:
            logger.info(f"Пробуем собрать CalendarDay из полей: day_data={day_data}, note={note}")
            calendar_day = CalendarDay(
                date=day_data.date,
                type_id=day_data.type_id,
                type_text=self._day_types[day_data.type_id - 1],
                note=note,
                week_day=self._week_days[day_data.date.weekday()]
            )
            if calendar_day:
                logger.info(f"CalendarDay (из полей: day_data={day_data}, note={note}) успешно собран: {calendar_day}")
                return calendar_day
            logger.warning(f"При сборке CalendarDay (из полей: day_data={day_data}, note={note}) что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При сборке CalendarDay (из полей: day_data={day_data}, note={note}) произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def create_day(self, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Создаёт календарный день
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
            correct_day = self._assemble_day(day_data, note)
            created_day = await self._repo.create_day(correct_day)
            if created_day:
                logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
                return created_day
            logger.warning("При создании календарного дня что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def update_day(self, date: datetime.date, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Обновляет календарный день по date
        """

        try:
            logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
            new_day = self._assemble_day(day_data, note)
            updated_day = await self._repo.update_day(date, new_day)
            if updated_day:
                logger.info(f"Календарный день date={date} успешно обновлён (после валидации): {updated_day}")
                return updated_day
            logger.warning(f"При обновлении календарного дня date={date} что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При обновлении календарного дня date={date} произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def delete_day(self, date: datetime.date) -> bool:
        """
        ### Удаляет календарный день по date
        """

        try:
            logger.info(f"Пробуем удалить календарный день date={date}")
            deleted_status = await self._repo.delete_day(date)
            if deleted_status:
                logger.info(f"Календарный день date={date} успешно удалён")
                return True
            logger.warning(f"При удалении календарного дня date={date} что-то пошло не так")
            return False
        except Exception as e:
            logger.error(f"При удалении календарного дня date={date} произошла ошибка: {str(e)}", exc_info=True)
            return False