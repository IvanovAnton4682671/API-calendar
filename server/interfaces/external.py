from core.logger import setup_logger
from core.config import settings
from httpx import AsyncClient, Response

logger = setup_logger("interfaces.external")

class ExternalInterface:
    """Интерфейс взаимодействия с внешним ресурсом

    Класс описывает интерфейс для взаимодействия с внешним ресурсом isdayoff.ru

    Example:
        >>>external_interface = ExternalInterface()
    """

    def __init__(self):
        """Конструктор класса

        Создаёт экземпляр класса для работы с внешним источником данных

        Args:
            self (Self@ExternalInterface): Экземпляр класса
        """
        self._base_url = f"{settings.EXTERNAL_URL}"
        self._client = AsyncClient()

    async def get_days_by_year(self, year: str, week_type: int) -> str:
        """GET-запрос на получение данных

        Выполняет GET-запрос на ресурс isdayoff.ru, после чего возвращает полученную строку дней формата "10010101",
        где 0 - рабочий день, 1 - нерабочий

        Args:
            self (Self@ExternalInterface): Экземпляр класса
            year (int): Год, за который получает список дней
            week_type (int): Тип рабочей недели

        Returns:
            str: Контент ответа в виде одной строки

        Examples:
            >>>result = await external_interface.get_days_bu_year("2025", 5)
        """

        try:
            logger.info(f"Отправляем запрос на url={self._base_url} с годом={year} и типом недели={week_type}")
            sd = 0 if week_type == 5 else 1
            request_url = f"{self._base_url}/api/getdata?year={year}&sd={str(sd)}"
            response = await self._client.get(request_url)
            return str(response.json())
        except Exception as e:
            logger.error(f"При выполнении запроса на url={request_url} произошла ошибка: {str(e)}")
            raise e