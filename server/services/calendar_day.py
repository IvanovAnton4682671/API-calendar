from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from core.consts import DAY_TYPES, WEEK_DAYS
from schemas.calendar_day import CalendarDayInput, CalendarDayInDB
from typing import Optional
from models.calendar_day import CalendarDay

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

    async def create_day(self, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Вычисляет необходимые поля и создаёт календарный день
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
            correct_day = CalendarDay(
                date=day_data.date,
                type_id=day_data.type_id,
                type_text=self._day_types[day_data.type_id - 1],
                note=note,
                week_day=self._week_days[day_data.date.weekday()]
            )
            created_day = await self._repo.create_day(correct_day)
            if created_day:
                logger.info(f"Календарный день успешно создан: {created_day}")
                return created_day
            logger.warning("При создании календарного дня что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
            raise