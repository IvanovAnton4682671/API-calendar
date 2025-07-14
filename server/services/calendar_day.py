from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from schemas.calendar_day import CalendarDayInput, CalendarDayInDB
from typing import Optional
from services.calendar_day_utils import assemble_day, period_parse, create_base_days, merge_days, formatting_days, get_statistic
from datetime import date

logger = setup_logger("services.calendar_day")

class CalendarDayService:
    """Сервис бизнес-логики календарных дней

    Класс описывает основные бизнес-методы для обработки данных при работе с календарными днями

    Args:
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Examples:
        >>>service = CalendarDayService(session)
    """

    def __init__(self, session: AsyncSession) -> None:
        """Конструктор класса

        Создаёт экземпляр класса для работы с асинхронной сессией БД PostgreSQL

        Args:
            self (Self@CalendarDayService): Экземпляр класса
            session (AsyncSession): Асинхронная сессия для выполнения запросов к БД
        """

        self._repo = CalendarDayRepository(session)

    async def create_day(self, day_data: CalendarDayInput, note: Optional[str]) -> CalendarDayInDB:
        """Создаёт календарный день

        Собирает модель календарного дня из полученных данных CalendarDayInput и создаёт день

        Args:
            self (Self@CalendarDayService): Экземпляр класса
            day_data (CalendarDayInput): Данные для создания дня
            note (Optional[str]): Опциональное описание дня

        Returns:
            CalendarDayInDB: Представление созданного календарного дня в БД

        Raises:
            Exception: В непредвиденной ситуации

        Example:
            >>>created_day = await service.create_day(CalendarDayInput(date=...,...))
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: day_data={day_data}, note={note}")
            correct_day = assemble_day(day_data, note)
            created_day = await self._repo.create_day(correct_day)
            logger.info(f"Календарный день успешно создан (после валидации): {created_day}")
            return created_day
        except Exception as e:
            desc = f"При создании календарного дня с данными: day_data={day_data}, note={note} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    async def get_days_by_period(self, period: str, compact: bool, week_type: int, statistic: bool) -> dict:
        """Получает календарные дни по периоду

        Динамически создаёт полный список дней обычного календаря от параметра week_type для периода period,
        далее получает дни для этого же периода из БД и перезаписывает соответствующие стандартные дни полученными,
        после чего форматирует итоговый список дней в нужный вид

        Args:
            self (Self@CalendarDayService): Экземпляр класса
            period (str): Произвольный формат периода
            compact (bool): Формат итоговых данных (True - компактный, False - полный)
            week_type (int): Тип недели календаря (5- или 6-дневная)
            statistic (bool): Формат статистики (True - детальная, False - обычная)

        Returns:
            dict: Форматированный словарь с множеством параметров

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>result = await service.get_days_by_period("2025", False, 5, True)
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
                result.update(add_statistic)
                logger.info(f"Итоговый результат сформирован")
            result["days"] = result_days
            return result
        except Exception as e:
            desc = f"При получении календарных дней по периоду={period} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    async def update_day(self, date: date, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """Обновляет календарный день по дате

        Обновляет календарный день по дате date данными day_data и note

        Args:
            self (Self@CalendarDayService): Экземпляр класса
            date (date): Дата обновляемого дня
            day_data(CalendarDayInput): Данные для обновления календарного дня
            note (Optional[str]): Опциональное описание дня

        Returns:
            Optional[CalendarDayInDB]: Обновлённый календарный день, если такой день был, иначе None

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>updated_day = await service.update_day(date(2025, 1, 1), CalendarDayInput(date=...,...), "Описание")
        """

        try:
            logger.info(f"Пробуем обновить календарный день date={date} данными: day_data={day_data}, note={note}")
            new_day = assemble_day(day_data, note)
            updated_day = await self._repo.update_day(date, new_day)
            if updated_day:
                logger.info(f"Календарный день date={date} успешно обновлён (после валидации): {updated_day}")
                return updated_day
            else:
                logger.warning(f"Календарный день date={date} не существует")
                return None
        except Exception as e:
            desc = f"При обновлении календарного дня date={date} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    async def delete_day(self, date: date) -> bool:
        """Удаляет календарный день по дате

        Удаляет календарный день по дате date

        Args:
            self (Self@CalendarDayService): Экземпляр класса
            date (date): Дата удаляемого дня

        Returns:
            bool: Статус удалённого дня (True - день удалён, False - день не существует)

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>deleted_day = await service.delete_day(date(2025, 1, 1))
        """

        try:
            logger.info(f"Пробуем удалить календарный день date={date}")
            deleted_status = await self._repo.delete_day(date)
            if deleted_status:
                logger.info(f"Календарный день date={date} успешно удалён")
                return True
            else:
                logger.warning(f"Календарный день date={date} не существует")
                return False
        except Exception as e:
            desc = f"При удалении календарного дня date={date} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)