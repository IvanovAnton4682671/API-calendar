from core.logger import setup_logger
from bs4 import BeautifulSoup
from core.consts import MONTHS, OFFICIAL_HOLIDAYS, WEEK_DAYS, DAY_TYPES
from datetime import date

logger = setup_logger("services.external_utils")

def parse_consultant_calendar(response_text: str, year: int, week_type: int) -> list[dict]:
    """Парсит HTML для получения календарных дней

    Парсит HTML-страницу, полученную от Консультанта, и ищет в ней календарные дни,
    после чего составляет список таких календарных дней

    Args:
        response_text (str): HTML-страница Консультанта
        year (int): Год запрашиваемого календаря
        week_type (int): тип рабочей недели

    Returns:
        list[dict]: Сформированный список календарных дней

    Raises:
        Exception: В непредвиденной ситуации

    Example:
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
                    if cell_classes == "inactively": #пропускаем пустую ячейку таблицы
                        continue
                    day_str = cell.get_text(strip=True)
                    day_text = "".join(d for d in day_str if d.isdigit()) #отбрасываем все прочие символы кроме цифр
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
        logger.error(f"При парсинге календаря Консультанта произошла ошибка: {str(e)}", exc_info=True)
        raise e

def get_statistic(correct_external_days: list[dict]) -> dict:
    """Формирует статистику

    Формирует дополнительную статистику по списку календарных дней

    Args:
        correct_external_days (list[dict]): Сформированный список календарных дней

    Returns:
        dict: Сформированная статистика

    Raises:
        Exception: В непредвиденной ситуации

    Example:
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
        logger.error(f"При формировании статистики произошла ошибка: {str(e)}", exc_info=True)
        raise e