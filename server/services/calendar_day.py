from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from schemas.calendar_day import CalendarDayInput, CalendarDayInDB
from typing import Optional
from services.calendar_day_utils import create_base_days, merge_days, assemble_day, period_parse, formatting_days, get_statistic
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

    async def create_day(self, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Создаёт календарный день
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
            correct_day = assemble_day(day_data, note)
            created_day = await self._repo.create_day(correct_day)
            if created_day:
                logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
                return created_day
            logger.warning("При создании календарного дня что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При создании календарного дня произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def get_days_by_period(self, period: str, compact: bool, week_type: int, statistic: bool) -> Optional[dict]:
        """
        ### Получает календарные дни по периоду
        """

        try:
            logger.info(f"Пробуем получить календарные дни по периоду={period}")
            date_start, date_end, period_name = period_parse(period)
            base_days = create_base_days(date_start, date_end, week_type)
            db_days = await self._repo.get_days_by_period(date_start, date_end)
            merged_days = merge_days(base_days, db_days)
            result_days = formatting_days(merged_days, compact, week_type)
            result = {
                "date_start": date_start.strftime("%d.%m.%Y"),
                "date_end": date_end.strftime("%d.%m.%Y"),
                "work_week_type": f"{week_type}-и дневная рабочая неделя",
                "period": period_name,
            }
            if statistic:
                add_statistic = get_statistic(merged_days)
                if add_statistic:
                    result.update(add_statistic)
            result["days"] = result_days
            return result
        except Exception as e:
            logger.error(f"При получении календарных дней по периоду={period} произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def update_day(self, date: datetime.date, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Обновляет календарный день по дате
        """

        try:
            logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
            new_day = assemble_day(day_data, note)
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
        ### Удаляет календарный день по дате
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