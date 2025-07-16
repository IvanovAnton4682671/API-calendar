from core.logger import setup_logger
from datetime import date, timedelta
from core.consts import DAY_TYPES, WEEK_DAYS

logger = setup_logger("services.external_utils")

def external_days_parse(external_days: str, date_start: date, week_type: int) -> list[dict]:
    """Превращает строку в массив дней

    Парсит строку вида "000011010" в список словарей, где каждый словарь - день

    Args:
        external_days (str): Исходная строка дней
        date_start (date): Дата начала периода
        week_type (int): Тип рабочей недели

    Returns:
        list[dict]: Форматированный список дней

    Example:
        >>>correct_externals_days = external_days_parse("0001010", date(2025, 1, 1), 5)
    """

    try:
        correct_external_days: list[dict] = []
        cur_date = date_start
        type_id = None
        type_text = None
        note = None
        weekends = ["сб", "вс"] if week_type == 5 else ["вс"]
        for day in external_days:
            if day == "0":
                type_id = 1
                type_text = DAY_TYPES[type_id]
                note = "Обычный рабочий день"
            elif day == "1":
                week_day = WEEK_DAYS[cur_date.weekday()]
                if week_day in weekends:
                    type_id = 2
                    note = "Обычный выходной день"
                elif week_day not in weekends:
                    type_id = 3
                    note = "Государственный праздник"
                type_text = DAY_TYPES[type_id]
            correct_external_day = {
                "date": cur_date.strftime("%d.%m.%Y"),
                "type_id": type_id,
                "type_text": type_text,
                "note": note,
                "week_day": WEEK_DAYS[cur_date.weekday()]
            }
            correct_external_days.append(correct_external_day)
            cur_date += timedelta(days=1)
        return correct_external_days
    except Exception as e:
        logger.error(f"При парсинге календарных дней произошла ошибка: {str(e)}")
        raise e

def get_statistic(correct_external_days: list[dict]) -> dict:
    """Формирует дополнительную статистику

    Формирует подробную статистику по форматированному списку дней

    Args:
        correct_external_days (list[dict]): Форматированный список дней

    Returns:
        dict: Словарь подробной статистики

    Example:
        >>>add_statistic = get_statistic([{'date': ...,...},...])
    """

    try:
        calendar_days = len(correct_external_days)
        work_days, weekends, holidays = 0, 0, 0
        for day in correct_external_days:
            if day["type_id"] == 1:
                work_days += 1
                continue
            elif day["type_id"] == 2:
                weekends += 1
                continue
            elif day["type_id"] == 3:
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