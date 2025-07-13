from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from core.consts import DAY_TYPES, WEEK_DAYS
from schemas.calendar_day import CalendarDayInput, CalendarDayInDB
from typing import Optional, Tuple, List
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

    def _period_parse(self, period: str) -> Tuple[datetime.date, datetime.date, str]:
        """
        ### Превращает произвольный период в даты начала и конца
        """

        def parse_date(date_str: str) -> datetime.date:
            """
            ### Парсит строковую дату формата `ДД.ММ.ГГГГ` в `datetime.date`
            """

            try:
                logger.info(f"Пробуем парсить строковую дату={date_str}")
                parts = date_str.split(".")
                if len(parts) != 3:
                    desc = f"Строковая дата должна иметь вид ДД.ММ.ГГГГ, но имеет вид {date_str}"
                    logger.warning(desc)
                    raise ValueError(desc)
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                return datetime.date(year, month, day)
            except Exception as e:
                desc = f"При парсинге строковой даты={date_str} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)

        try:
            #произвольный период ДД.ММ.ГГГГ-ДД.ММ.ГГГГ
            try:
                if "-" in period:
                    parts = period.split("-")
                    if len(parts) != 2:
                        desc = f"Произвольный период должен иметь вид ДД.ММ.ГГГГ-ДД.ММ.ГГГГ, но имеет вид {period}"
                        logger.warning(desc)
                        raise ValueError(desc)
                    date_start = parse_date(parts[0])
                    date_end = parse_date(parts[1])
                    if date_start > date_end:
                        date_start, date_end = date_end, date_start
                    return date_start, date_end, "Произвольный период"
            except Exception as e:
                desc = f"При парсинге произвольного периода={period} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)
            #квартал QNГГГГ
            try:
                if period.startswith("Q"):
                    if len(period) != 6 or not period[1:].isdigit():
                        desc = f"Квартал должен иметь вид QNГГГГ, но имеет вид {period}"
                        logger.warning(desc)
                        raise ValueError(desc)
                    quarter = int(period[1])
                    year = int(period[2:])
                    if quarter < 1 or quarter > 4:
                        desc = f"Квартал должен быть от 1 до 4, но получен {str(quarter)}"
                        logger.warning(desc)
                        raise ValueError(desc)
                    start_month = 3 * (quarter - 1) + 1
                    end_month = start_month + 2
                    date_start = datetime.date(year, start_month, 1)
                    if end_month == 12:
                        date_end = datetime.date(year, end_month, 31)
                    else:
                        date_end = datetime.date(year, end_month + 1, 1) - datetime.timedelta(days=1)
                    return date_start, date_end, "Квартал"
            except Exception as e:
                desc = f"При парсинге квартала={period} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)
            #сутки ДД.ММ.ГГГГ
            try:
                if period.count(".") == 2:
                    date_start = parse_date(period)
                    return date_start, date_start, "Сутки"
            except Exception as e:
                desc = f"При парсинге суток={period} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)
            #месяц ММ.ГГГГ
            try:
                if period.count(".") == 1:
                    parts = period.split(".")
                    if len(parts) != 2 or len(parts[0]) != 2 or len(parts[1]) != 4:
                        desc = f"Месяц должен иметь вид ММ.ГГГГ, но имеет вид {period}"
                        logger.warning(desc)
                        raise ValueError(desc)
                    month = int(parts[0])
                    year = int(parts[1])
                    if month < 1 or month > 12:
                        desc = f"Месяц должен быть от 01 до 12, но получен {month}"
                        logger.warning(desc)
                        raise ValueError(desc)
                    date_start = datetime.date(year, month, 1)
                    if month == 12:
                        date_end = datetime.date(year, month, 1)
                    else:
                        date_end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
                    return date_start, date_end, "Месяц"
            except Exception as e:
                desc = f"При парсинге месяца={period} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)
            #год ГГГГ
            try:
                if len(period) == 4 and period.isdigit():
                    year = int(period)
                    date_start = datetime.date(year, 1, 1)
                    date_end = datetime.date(year, 12, 31)
                    return date_start, date_end, "Год"
            except Exception as e:
                desc = f"При парсинге года={period} произошла ошибка: {str(e)}"
                logger.error(desc, exc_info=True)
                raise ValueError(desc)
            desc = f"Получен неизвестный формат периода={period}"
            logger.warning(desc)
            raise ValueError(desc)
        except Exception as e:
            logger.error(f"При парсинге period={period} произошла ошибка: {str(e)}", exc_info=True)
            return None

    def _formatting_list_of_days(self, list_of_days: List[CalendarDayInDB], compact: bool, week_type: int) -> Optional[List[CalendarDayInDB]]:
        """
        ### Форматирует итоговый список календарных дней в зависимости от параметров compact и week_type
        """

        try:
            formatted_list_of_days: List[CalendarDayInDB] = []
            for day in list_of_days:
                day.date = day.date.strftime("%d.%m.%Y")
                formatted_list_of_days.append(day)
            if compact:
                specials_days: List[CalendarDayInDB] = []
                weekend = ["сб", "вс"] if week_type == 5 else ["вс"]
                for day in formatted_list_of_days:
                    if day.note:
                        specials_days.append(day)
                        continue
                    if day.type_id == 3:
                        specials_days.append(day)
                        continue
                    if (day.type_id == 1 and day.week_day in weekend) or (day.type_id == 2 and day.week_day not in weekend):
                        specials_days.append(day)
                for day in specials_days:
                    if day.note is None:
                        del day.note
                return specials_days
            for day in formatted_list_of_days:
                if day.note is None:
                    del day.note
            return formatted_list_of_days
        except Exception as e:
            logger.error(f"При форматировании списка календарных дней произошла ошибка: {str(e)}", exc_info=True)
            return None

    def _get_dop_statistic(self, list_of_days: List[CalendarDayInDB]) -> Optional[dict]:
        """
        ### Формирует дополнительную статистику по списку календарных дней
        """

        try:
            calendar_days = len(list_of_days)
            work_days, weekends, holidays = 0, 0, 0
            for day in list_of_days:
                if day.type_id == 1:
                    work_days += 1
                elif day.type_id == 2:
                    weekends += 1
                elif day.type_id == 3:
                    holidays += 1
            return {
                "calendar_days": calendar_days,
                "calendar_days_without_holidays": calendar_days - holidays,
                "work_days": work_days,
                "weekends": weekends,
                "holidays": holidays
            }
        except Exception as e:
            logger.error(f"При формировании дополнительной статистики произошла ошибка: {str(e)}", exc_info=True)
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

    async def get_days_by_period(self, period: str, compact: bool, week_type: int, statistic: bool) -> Optional[dict]:
        """
        ### Получает календарные дни по периоду
        """

        try:
            logger.info(f"Пробуем получить календарные дни по периоду={period}")
            date_start, date_end, period_name = self._period_parse(period)
            list_of_days = await self._repo.get_days_by_period(date_start, date_end)
            if list_of_days:
                logger.info(f"Календарные дни по периоду={period} успешно получены, их {len(list_of_days)}")
                new_list_of_days = self._formatting_list_of_days(list_of_days, compact, week_type)
                result = {
                    "date_start": date_start.strftime("%d.%m.%Y"),
                    "date_end": date_end.strftime("%d.%m.%Y"),
                    "work_week_type": f"{week_type}-и дневная рабочая неделя",
                    "period": period_name,
                }
                if statistic:
                    dop_statistic = self._get_dop_statistic(list_of_days)
                    if dop_statistic:
                        result.update(dop_statistic)
                result["days"] = new_list_of_days
                return result
            logger.warning(f"При получении календарных дней по периоду={period} что-то пошло не так")
            return None
        except Exception as e:
            logger.error(f"При получении календарных дней по периоду={period} произошла ошибка: {str(e)}", exc_info=True)
            return None

    async def update_day(self, date: datetime.date, day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDayInDB]:
        """
        ### Обновляет календарный день по дате
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