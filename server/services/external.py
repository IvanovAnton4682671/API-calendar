from core.logger import setup_logger
from services.calendar_day_utils import period_parse
from interfaces.external import ExternalInterface
from services.external_utils import parse_consultant_calendar, get_statistic
from datetime import datetime

logger = setup_logger("service.external")

class ExternalService:
    """Сервис бизнес-логики внешних ресурсов

    Класс описывает бизнес-методы для получения календарных дней из внешних ресурсов

    Examples:
        >>>external_service = ExternalService()
    """

    def __init__(self) -> None:
        """Конструктор класса

        Создаёт экземпляр класса для работы с внешним источником данных

        Args:
            self (Self@ExternalService): Экземпляр класса
        """

        pass

    async def get_days_by_year(self, year: int, week_type: int, statistic: bool) -> dict:
        """Формирует список календарных дней из внешних данных

        Получает список календарных дней, полученных после парсинга HTML-страницы Консультанта или HH.ru,
        после чего форматирует его и возвращает

        Args:
            self (Self@ExternalService): Экземпляр класса
            year (int): Год запрашиваемого календаря
            week_type (int): Тип рабочей недели
            statistic (bool): Опциональная статистика календаря

        Returns:
            dict: Словарь с календарём и дополнительными данными

        Raises:
            Exception: В непредвиденной ситуации

        Example:
            >>>result = await external_service.get_days_by_year(2025, 5, True)
        """

        try:
            logger.info(f"Пробуем сформировать календарь (year={year}, week_type={week_type}, statistic={statistic})")
            if year >= 2017:
                if year > datetime.now().year:
                    raise ValueError(f"Год должен быть не больше текущего, не получен {year}")
                year_str = str(year)
                date_start, date_end, period_name = period_parse(year_str)
                external_interface = ExternalInterface()
                if year_str == "2024":
                    year_str = "2024b"
                response_text = await external_interface.get_consultant_calendar(year_str)
                correct_external_days = parse_consultant_calendar(response_text, year, week_type)
                result = {
                    "date_start": date_start.strftime("%d.%m.%Y"),
                    "date_end": date_end.strftime("%d.%m.%Y"),
                    "work_week_type": f"{week_type}-дневная рабочая неделя",
                    "period": period_name,
                }
                if statistic:
                    add_statistic = get_statistic(correct_external_days)
                    result.update(add_statistic)
                result["days"] = correct_external_days
                return result
            else:
                pass
        except Exception as e:
            logger.error(f"При получении календарных дней (year={year}, week_type={week_type}) произошла ошибка: {str(e)}", exc_info=True)
            raise e