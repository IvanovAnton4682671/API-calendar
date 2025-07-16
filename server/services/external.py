from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.calendar_day import CalendarDayRepository
from services.calendar_day_utils import period_parse
from interfaces.external import ExternalInterface
from services.external_utils import external_days_parse, get_statistic
from datetime import datetime

logger = setup_logger("service.external")

class ExternalService:
    """Сервис бизнес-логики внешнего ресурса

    Класс описывает бизнес-методы для получения календарных дней из внешнего источника

    Examples:
        >>>service = ExternalService()
    """

    def __init__(self) -> None:
        """Конструктор класса

        Создаёт экземпляр класса для работы с внешним источником данных

        Args:
            self (Self@ExternalService): Экземпляр класса
        """

        pass

    async def get_days_by_year(self, year: int, week_type: int, statistic: bool) -> dict:
        """Получает календарные дни за год

        Получает список календарных дней из внешнего источника, после чего форматирует список

        Args:
            self (Self@ExternalService): Экземпляр класса
            year (int): Год, за который получает список дней
            week_type (int): Тип рабочей недели
            statistic (bool): Формат формируемой статистики

        Returns:
            dict: Форматированный словарь с множеством параметров

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>result = await service.get_days_by_year(2025)
        """

        try:
            logger.info(f"Пробуем получить календарные дни по параметрам: год={year}, рабочая неделя={week_type}")
            if year < 2004 or year > datetime.now().year:
                raise ValueError(f"Год должен быть от 2004 и до текущего, но получен {year}")
            date_start, date_end, period_name = period_parse(str(year))
            external_interface = ExternalInterface()
            external_days = await external_interface.get_days_by_year(str(year), week_type)
            correct_external_days = external_days_parse(external_days, date_start, week_type)
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
        except Exception as e:
            logger.error(f"При получении календарных дней за год={year} произошла ошибка: {str(e)}", exc_info=True)
            raise e