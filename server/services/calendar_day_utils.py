from core.logger import setup_logger
from schemas.calendar_day import BaseCalendarDay, CalendarDayInput, CalendarDayInDB
from typing import Optional, Union
from models.calendar_day import CalendarDay
from core.consts import DAY_TYPES, WEEK_DAYS
from datetime import date, timedelta

logger = setup_logger("services.calendar_day_utils")

def assemble_day(day_data: CalendarDayInput, note: Optional[str]) -> CalendarDay:
    """Собирает календарный день

    Собирает календарный день CalendarDay из его полей

    Args:
        day_data (CalendarDayInput): Данные для создания дня
        note (Optional[str]): Опциональное описание дня

    Returns:
        CalendarDay: Собранная модель календарного дня

    Raises:
        Exception: В непредвиденной ситуации

    Examples:
        >>>correct_day = assemble_day(CalendarDayInput(date=...,...), "Описание")
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
        return calendar_day
    except Exception as e:
        desc = f"При сборке CalendarDay (из полей: day_data={day_data}, note={note}) произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def period_parse(period: str) -> tuple[date, date, str]:
    """Парсит строку периода в даты начала и конца

    Парсит строку периода в даты начала и конца, а также возвращает наименование периода
    Поддерживаемые форматы периода:
    - Год: ГГГГ
    - Квартал: QNГГГГ
    - Месяц: ММ.ГГГГ
    - Сутки: ДД.ММ.ГГГГ
    - Произвольный период: ДД.ММ.ГГГГ-ДД.ММ.ГГГГ

    Args:
        period (str): Временной период

    Returns:
        tuple[date, date, str]: Даты начала и конца, а также наименование периода

    Raises:
        ValueError: При некорректных данных
        Exception: В непредвиденной ситуации

    Example:
        >>>date_start, date_end, period_name = period_parse("2025")
    """

    def parse_date(date_str: str) -> date:
        """Парсит строковую дату в date

        Парсит строковую дату формата ДД.ММ.ГГГГ в date

        Args:
            date_str (str): Дата формата ДД.ММ.ГГГГ

        Returns:
            date: Дата формата date

        Raises:
            ValueError: При некорректных данных
            Exception: В непредвиденной ситуации

        Example:
            >>>correct_date = parse_date("01.01.2025")
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
            return date(year, month, day)
        except Exception as e:
            desc = f"При парсинге строковой даты={date_str} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

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
            raise Exception(desc)
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
                date_start = date(year, start_month, 1)
                if end_month == 12:
                    date_end = date(year, end_month, 31)
                else:
                    date_end = date(year, end_month + 1, 1) - timedelta(days=1)
                return date_start, date_end, "Квартал"
        except Exception as e:
            desc = f"При парсинге квартала={period} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)
        #сутки ДД.ММ.ГГГГ
        try:
            if period.count(".") == 2:
                date_start = parse_date(period)
                return date_start, date_start, "Сутки"
        except Exception as e:
            desc = f"При парсинге суток={period} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)
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
                date_start = date(year, month, 1)
                if month == 12:
                    date_end = date(year, month, 1)
                else:
                    date_end = date(year, month + 1, 1) - timedelta(days=1)
                return date_start, date_end, "Месяц"
        except Exception as e:
            desc = f"При парсинге месяца={period} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)
        #год ГГГГ
        try:
            if len(period) == 4 and period.isdigit():
                year = int(period)
                date_start = date(year, 1, 1)
                date_end = date(year, 12, 31)
                return date_start, date_end, "Год"
        except Exception as e:
            desc = f"При парсинге года={period} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)
        desc = f"Получен неизвестный формат периода={period}"
        logger.warning(desc)
        raise ValueError(desc)
    except Exception as e:
        desc = f"При парсинге period={period} произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def create_base_days(date_start: date, date_end: date, week_type: int) -> list[BaseCalendarDay]:
    """Создаёт обычный календарь по периоду

    Создаёт обычный календарь по периоду с date_start по date_end включительно с учётом week_type

    Args:
        date_start (date): Дата начала периода
        date_end (date): Дата конца периода
        week_type (int): Тип недели

    Returns:
        list[BaseCalendarDay]: Список обычных календарных дней

    Raises:
        Exception: В непредвиденной ситуации

    Example:
        >>>base_days = create_base_days(date(2025, 1, 1), date(2025, 12, 1), 5)
    """

    try:
        logger.info(f"Пробуем создать обычный календарь с date_start={date_start} по date_end={date_end} для week_type={week_type}")
        base_days: list[BaseCalendarDay] = []
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
            current += timedelta(days=1)
        return base_days
    except Exception as e:
        desc = f"При создании обычного календаря произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def merge_days(base_days: list[BaseCalendarDay], db_days: list[CalendarDayInDB]) -> list[Union[BaseCalendarDay, CalendarDayInDB]]:
    """Перезаписывает обычные календарные дни днями из БД

    Перезаписывает обычные календарные дни соответствующими днями из БД

    Args:
        base_days (list[BaseCalendarDay]): Обычные календарные дни
        db_days (list[CalendarDayInDB]): Календарные дни из БД

    Returns:
        list[Union[BaseCalendarDay, CalendarDayInDB]]: Список, содержащий дни обоих типов

    Raises:
        Exception: В непредвиденной ситуации

    Example:
        >>>merged_days = merge_days([BaseCalendarDay(date=...,...),...], [CalendarDayInDB(date=...,...),...])
    """

    try:
        merged_days: list[Union[BaseCalendarDay, CalendarDayInDB]] = []
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

def formatting_days(merged_days: list[Union[BaseCalendarDay, CalendarDayInDB]], compact: bool, week_type: int) -> list[Union[BaseCalendarDay, CalendarDayInDB]]:
    """Форматирует объединённый список дней

    Форматирует объединённый список дней в зависимости от параметров compact и week_type

    Args:
        merged_days (list[Union[BaseCalendarDay, CalendarDayInDB]]): Список объединённых дней
        compact (bool): Формат итоговых данных (True - компактный, False - полный)
        week_type (int): Тип недели календаря (5- или 6-дневная)

    Returns:
        list[Union[BaseCalendarDay, CalendarDayInDB]]: Список форматированных дней обоих форматов

    Raises:
        Exception: В непредвиденной ситуации

    Example:
        >>>formatted_days = formatting_days([BaseCalendarDay(date=...,...),...,CalendarDayInDB(date=...,...),...], False, 5)
    """

    try:
        formatted_days: list[Union[BaseCalendarDay, CalendarDayInDB]] = []
        for day in merged_days:
            if type(day) is CalendarDayInDB:
                del day.id
            day.date = day.date.strftime("%d.%m.%Y")
            formatted_days.append(day)
        if compact:
            specials_days: list[CalendarDayInDB] = []
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

def get_statistic(merged_days: list[Union[BaseCalendarDay, CalendarDayInDB]]) -> dict:
    """Дополнительная статистика списка дней

    Формирует дополнительную статистику по списку объединённых дней

    Args:
        merged_days (list[Union[BaseCalendarDay, CalendarDayInDB]]): Список объединённых дней

    Result:
        dict: Словарь статистики

    Raises:
        Exception: В непредвиденной ситуации

    Example:
        >>>statistic = get_statistic([BaseCalendarDay(date=...,...),...,CalendarDayInDB(date=...,...),...])
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