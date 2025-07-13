from core.logger import setup_logger
from schemas.calendar_day import BaseCalendarDay, CalendarDayInput, CalendarDayInDB
from typing import Optional, Tuple, List, Union
from models.calendar_day import CalendarDay
from core.consts import DAY_TYPES, WEEK_DAYS
import datetime

logger = setup_logger("services.calendar_day_utils")

def create_base_days(date_start: datetime.date, date_end: datetime.date, week_type: int) -> List[BaseCalendarDay]:
    """
    ### Создаёт обычный календарь с учётом week_type
    """

    try:
        logger.info(f"Пробуем создать обычный календарь с date_start={date_start} по date_end={date_end} для week_type={week_type}")
        base_days: List[BaseCalendarDay] = []
        current = date_start
        while current <= date_end:
            if week_type == 5:
                if current.weekday() not in (5, 6):
                    type_id = 1
                elif current.weekday() in (5, 6):
                    type_id = 2
            elif week_type == 6:
                if current.weekday() != 6:
                    type_id = 1
                elif current.weekday() == 6:
                    type_id = 2
            base_day = BaseCalendarDay(
                date=current,
                type_id=type_id,
                type_text=DAY_TYPES[type_id],
                week_day=WEEK_DAYS[current.weekday()]
            )
            base_days.append(base_day)
            current += datetime.timedelta(days=1)
        logger.info(f"Обычный календарь с date_start={date_start} по date_end={date_end} для week_type={week_type} успешно собран, в нём {len(base_days)} дней")
        return base_days
    except Exception as e:
        desc = f"При создании обычного календаря произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def merge_days(base_days: List[BaseCalendarDay], db_days: List[CalendarDayInDB]) -> List[Union[BaseCalendarDay, CalendarDayInDB]]:
    """
    ### Перезаписывает обычные дни днями из БД
    """

    try:
        merged_days: List[Union[BaseCalendarDay, CalendarDayInDB]] = []
        db_days_dict = {db_day.date: db_day for db_day in db_days}
        for base_day in base_days:
            if base_day.date in db_days_dict:
                db_day = db_days_dict[base_day.date]
                merged_days.append(db_day)
            else:
                merged_days.append(base_day)
        return merged_days
    except Exception as e:
        desc = f"При перезаписи дней произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def assemble_day(day_data: CalendarDayInput, note: Optional[str]) -> Optional[CalendarDay]:
    """
    ### Собирает календарный день `CalendarDay` из его полей
    """

    try:
        logger.info(f"Пробуем собрать CalendarDay из полей: day_data={day_data}, note={note}")
        calendar_day = CalendarDay(
            date=day_data.date,
            type_id=day_data.type_id,
            type_text=DAY_TYPES[day_data.type_id],
            note=note,
            week_day=WEEK_DAYS[day_data.date.weekday()]
        )
        if calendar_day:
            logger.info(f"CalendarDay (из полей: day_data={day_data}, note={note}) успешно собран: {calendar_day}")
            return calendar_day
        logger.warning(f"При сборке CalendarDay (из полей: day_data={day_data}, note={note}) что-то пошло не так")
        return None
    except Exception as e:
        logger.error(f"При сборке CalendarDay (из полей: day_data={day_data}, note={note}) произошла ошибка: {str(e)}", exc_info=True)
        return None

def period_parse(period: str) -> Tuple[datetime.date, datetime.date, str]:
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

def formatting_days(merged_days: List[Union[BaseCalendarDay, CalendarDayInDB]], compact: bool, week_type: int) -> List[Union[BaseCalendarDay, CalendarDayInDB]]:
    """
    ### Форматирует объединённый список дней в зависимости от параметров compact и week_type
    """

    try:
        formatted_days: List[Union[BaseCalendarDay, CalendarDayInDB]] = []
        for day in merged_days:
            if type(day) is CalendarDayInDB:
                del day.id
            day.date = day.date.strftime("%d.%m.%Y")
            formatted_days.append(day)
        if compact:
            specials_days: List[CalendarDayInDB] = []
            weekend = ["сб", "вс"] if week_type == 5 else ["вс"]
            for day in formatted_days:
                if type(day) is CalendarDayInDB and day.note:
                    specials_days.append(day)
                    continue
                if type(day) is CalendarDayInDB and day.type_id == 3:
                    specials_days.append(day)
                    continue
                if (day.type_id == 1 and day.week_day in weekend) or (day.type_id == 2 and day.week_day not in weekend):
                    specials_days.append(day)
            for day in specials_days:
                if type(day) is CalendarDayInDB:
                    if day.note is None:
                        del day.note
            return specials_days
        for day in formatted_days:
            if type(day) is CalendarDayInDB:
                if day.note is None:
                    del day.note
        return formatted_days
    except Exception as e:
        desc = f"При форматировании объединённого списка дней произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def get_statistic(merged_days: List[Union[BaseCalendarDay, CalendarDayInDB]]) -> dict:
    """
    ### Формирует статистику по списку объединённых дней
    """

    try:
        calendar_days = len(merged_days)
        work_days, weekends, holidays = 0, 0, 0
        for day in merged_days:
            if day.type_id == 1:
                work_days += 1
            elif day.type_id == 2:
                weekends += 1
            elif type(day) is CalendarDayInDB and day.type_id == 3:
                holidays += 1
        return {
            "calendar_days": calendar_days,
            "calendar_days_without_holidays": calendar_days - holidays,
            "work_days": work_days,
            "weekends": weekends,
            "holidays": holidays
        }
    except Exception as e:
        desc = f"При формировании статистик произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)