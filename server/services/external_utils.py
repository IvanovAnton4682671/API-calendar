from core.logger import setup_logger
from bs4 import BeautifulSoup
from core.consts import MONTHS, OFFICIAL_HOLIDAYS, WEEK_DAYS, DAY_TYPES
from datetime import date
from fastapi import HTTPException, status

logger = setup_logger("services.external_utils")

def parse_consultant_calendar(response_text: str, year: int, week_type: int) -> list[dict]:
    """Парсит HTML для получения календарных дней

    Парсит HTML-страницу, полученную от Консультанта, и ищет в ней календарные дни,
    после чего составляет список таких календарных дней

    Args:
        response_text (str): HTML-страница Консультанта
        year (int): Год запрашиваемого календаря
        week_type (int): Тип рабочей недели

    Returns:
        list[dict]: Сформированный список календарных дней

    Raises:
        HTTPException: В непредвиденной ситуации

    Examples:
        >>>correct_external_days = parse_consultant_calendar("...", 2025, 5)
    """

    try:
        soup = BeautifulSoup(response_text, "html.parser")
        calendar_tables = soup.select("table.cal")
        weekends = ["сб", "вс"] if week_type == 5 else ["вс"]
        correct_external_days: list[dict] = []
        for table in calendar_tables:
            month_header = table.find("th", class_="month")
            if not month_header:
                continue
            month_name = month_header.get_text(strip=True).lower()
            month_number = MONTHS.get(month_name)
            if not month_number:
                continue
            table_body = table.find("tbody")
            if not table_body:
                continue
            for row in table_body.find_all("tr"):
                for cell in row.find_all("td"):
                    cell_classes = cell.get("class", [])
                    if cell_classes == "inactively":
                        continue
                    day_str = cell.get_text(strip=True)
                    day_text = "".join(d for d in day_str if d.isdigit())
                    if not day_text:
                        continue
                    day_number = int(day_text)
                    day_date = date(year, month_number, day_number)
                    note = None
                    if "holiday" in cell_classes or (month_number, day_number) in OFFICIAL_HOLIDAYS.keys(): #официальный праздник перекрывается простым выходным, исправляем
                        type_id = 3
                        note = OFFICIAL_HOLIDAYS.get((month_number, day_number))
                    elif "weekend" in cell_classes: #при 6-дневной неделе выходная суббота перестаёт быть таковой
                        if WEEK_DAYS[day_date.weekday()] in weekends:
                            type_id = 2
                        else:
                            type_id = 1
                    elif "preholiday" in cell_classes:
                        type_id = 1
                        note = "Предпраздничный день"
                    else:
                        type_id = 1
                    correct_day = {
                        "date": day_date.strftime("%d.%m.%Y"),
                        "type_id": type_id,
                        "type_text": DAY_TYPES[type_id],
                    }
                    if note:
                        correct_day.update({"note": note})
                    correct_day.update({"week_day": WEEK_DAYS[day_date.weekday()]})
                    correct_external_days.append(correct_day)
        return correct_external_days
    except Exception as e:
        desc = f"При парсинге календаря Консультанта произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

def parse_hhru_calendar(response_text: str, year: int, week_type: int) -> list[dict]:
    """Парсит HTML для получения календарных дней

    Парсит HTML-страницу, полученную от hh.ru, и ищет в ней календарные дни,
    после чего составляет список таких календарных дней

    Args:
        response_text (str): HTML-страница hh.ru
        year (int): Год запрашиваемого календаря
        week_type (int): Тип рабочей недели

    Returns:
        list[dict]: Сформированный список календарных дней

    Raises:
        HTTPException: В непредвиденной ситуации

    Examples:
        >>>correct_external_days = parse_hhru_calendar("...", 2025, 5)
    """

    try:
        soup = BeautifulSoup(response_text, "html.parser")
        correct_external_days: list[dict] = []
        weekends = ["сб", "вс"] if week_type == 5 else ["вс"]
        calendar_quarters = soup.select("ul.calendar-list")
        for quarter in calendar_quarters:
            months_list = quarter.find_all("li", class_="calendar-list__item")
            if not months_list:
                continue
            for month in months_list:
                month_body = month.find("div", class_="calendar-list__item-body")
                if not month_body:
                    continue
                month_title = month_body.find("div", class_="calendar-list__item-title")
                if not month_title:
                    continue
                month_name = month_title.get_text(strip=True).lower()
                month_number = MONTHS.get(month_name)
                if not month_number:
                    continue
                days_table = month_body.find("ul", class_="calendar-list__numbers")
                if not days_table:
                    continue
                days_list = days_table.find_all("li")
                for day in days_list:
                    day_classes = day.get("class", [])
                    if "calendar-list__numbers__item_other" in day_classes:
                        continue
                    day_str = day.find(text=True, recursive=False)
                    day_text = "".join(d for d in day_str if d.isdigit())
                    if not day_text:
                        continue
                    if "час" in day_str:
                        if len(day_text) == 3:
                            day_number = int(day_text[0:2])
                        elif len(day_text) == 2:
                            day_number = int(day_text[0])
                    else:
                        day_number = int(day_text)
                    day_date = date(year, month_number, day_number)
                    note = None
                    if "calendar-list__numbers__item_day-off" in day_classes and (month_number, day_number) in OFFICIAL_HOLIDAYS.keys():
                        type_id = 3
                        note = OFFICIAL_HOLIDAYS.get((month_number, day_number))
                    elif "calendar-list__numbers__item_day-off" in day_classes:
                        if WEEK_DAYS[day_date.weekday()] not in weekends and week_type == 5:
                            type_id = 3
                        elif WEEK_DAYS[day_date.weekday()] in weekends:
                            type_id = 2
                        elif WEEK_DAYS[day_date.weekday()] == "сб" and week_type == 6:
                            type_id = 1
                    elif "calendar-list__numbers__item_shortened" in day_classes:
                        type_id = 1
                        note = "Предпраздничный день"
                    else:
                        type_id = 1
                    correct_day = {
                        "date": day_date.strftime("%d.%m.%Y"),
                        "type_id": type_id,
                        "type_text": DAY_TYPES[type_id],
                    }
                    if note:
                        correct_day.update({"note": note})
                    correct_day.update({"week_day": WEEK_DAYS[day_date.weekday()]})
                    correct_external_days.append(correct_day)
        return correct_external_days
    except Exception as e:
        desc = f"При парсинге календаря hh.ru произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

def get_statistic(correct_external_days: list[dict]) -> dict:
    """Формирует статистику

    Формирует дополнительную статистику по списку календарных дней

    Args:
        correct_external_days (list[dict]): Сформированный список календарных дней

    Returns:
        dict: Сформированная статистика

    Raises:
        HTTPException: В непредвиденной ситуации

    Examples:
        >>>add_statistic = get_statistic([{...},...])
    """

    try:
        calendar_days = len(correct_external_days)
        work_days, weekends, holidays = 0, 0, 0
        for day in correct_external_days:
            day_type_id = day.get("type_id")
            if day_type_id == 1:
                work_days += 1
            elif day_type_id == 2:
                weekends += 1
            elif day_type_id == 3:
                holidays += 1
        return {
            "calendar_days": calendar_days,
            "calendar_days_without_holidays": calendar_days - holidays,
            "work_days": work_days,
            "weekends": weekends,
            "holidays": holidays
        }
    except Exception as e:
        desc = f"При формировании статистики произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )