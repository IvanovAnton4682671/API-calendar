from core.logger import setup_logger
from core.config import settings
from httpx import AsyncClient

logger = setup_logger("interfaces.external")

class ExternalInterface:
    """Интерфейс взаимодействия с внешними ресурсами

    Класс представляет собой интерфейс взаимодействия с внешними ресурсами, которые предоставляют данные производственных календарей

    Example:
        >>>external_interface = ExternalInterface()
    """

    def __init__(self) -> None:
        """Конструктор класса

        Создаёт экземпляр класса для отправки запросов внешним источникам данных

        Args:
            self (Self@ExternalInterface): Экземпляр класса
        """

        self._consultant_url = settings.CONSULTANT_CALENDAR_URL
        self._hhru_url = settings.HHRU_CALENDAR_URL

    async def get_consultant_calendar(self, year_str: str) -> str:
        """GET-запрос к Консультанту

        Выполняет асинхронный GET-запрос с эмуляцией браузерного запроса для получения HTML-страницы производственного календаря от Консультанта

        Args:
            self (Self@ExternalInterface): Экземпляр класса
            year_str (str): Год в формате строки

        Returns:
            str: HTML-страница в формате строки

        Raises:
            Exception: В непредвиденной ситуации

        Example:
            >>>response_text = await external_interface.get_consultant_calendar("2025")
        """

        async with AsyncClient() as client:
            try:
                url = f"{self._consultant_url}/law/ref/calendar/proizvodstvennye/{year_str}/"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.error(f"При выполнении GET-запрос на url={url} произошла ошибка: {str(e)}", exc_info=True)
                raise e

    async def get_hhru_calendar(self, year_str: str) -> str:
        """GET-запрос к hh.ru

        Выполняет асинхронный GET-запрос с эмуляцией браузерного запроса для получения HTML-страницы производственного календаря от hh.ru

        Args:
            self (Self@ExternalInterface): Экземпляр класса
            year_str (str): Год в формате строки

        Returns:
            str: HTML-страница в формате строки

        Raises:
            Exception: В непредвиденной ситуации

        Example:
            >>>response_text = await external_interface.get_hhru_calendar("2025")
        """

        async with AsyncClient() as client:
            try:
                url = f"{self._hhru_url}/article/calendar{year_str}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = await client.get(url, headers=headers, follow_redirects=True)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.error(f"При выполнении GET-запроса на url={url} произошла ошибка: {str(e)}", exc_info=True)
                raise e