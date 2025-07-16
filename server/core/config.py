from core.logger import setup_logger
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, computed_field

logger = setup_logger("core.config")

class Settings(BaseSettings):
    """Для работы с переменными окружения

    Класс предназначен для удобной работы со всеми переменными окружение
    без нужды подгружать их через dotenv

    Attributes:
        POSTGRESQL_HOST (str): Хост подключения к PostgreSQL
        POSTGRESQL_PORT (int): Порт подключения к PostgreSQL
        POSTGRESQL_USER (str): Логин пользователя PostgreSQL
        POSTGRESQL_PASSWORD (SecretStr): Пароль пользователя PostgreSQL
        POSTGRESQL_DB (str): Название БД PostgreSQL
        POSTGRESQL_URL (SecretStr): Адрес подключения к PostgreSQL
        APP_NAME (str): Имя запускаемого экземпляра сервера
        APP_HOST (str): Хост сервера
        APP_PORT (int): Порт сервера
        APP_DEBUG (bool): Флаг отладки сервера
        EXTERNAL_URL (str): URL-адрес внешнего сервиса, который предоставляет данные производственного календаря

    Examples:
        >>>settings = Settings()
        >>>host = settings.POSTGRESQL_HOST
    """

    POSTGRESQL_HOST: str = Field(
        ...,
        min_length=1,
        description="Хост подключения к PostgreSQL"
    )
    POSTGRESQL_PORT: int = Field(
        ...,
        ge=1,
        le=65535,
        description="Порт подключения к PostgreSQL"
    )
    POSTGRESQL_USER: str = Field(
        ...,
        min_length=1,
        description="Логин пользователя PostgreSQL"
    )
    POSTGRESQL_PASSWORD: SecretStr = Field(
        ...,
        min_length=1,
        description="Пароль пользователя PostgreSQL"
    )
    POSTGRESQL_DB: str = Field(
        ...,
        min_length=1,
        description="Название БД PostgreSQL"
    )

    APP_NAME: str = Field(
        ...,
        min_length=1,
        description="Имя запускаемого экземпляра сервера"
    )
    APP_HOST: str = Field(
        ...,
        min_length=1,
        description="Хост сервера"
    )
    APP_PORT: int = Field(
        ...,
        ge=1,
        le=65535,
        description="Порт сервера"
    )
    APP_DEBUG: bool = Field(
        ...,
        description="Флаг отладки сервера"
    )

    EXTERNAL_URL: str = Field(
        ...,
        min_length=1,
        description="URL-адрес внешнего сервиса, который предоставляет данные производственного календаря"
    )

    @computed_field
    @property
    def POSTGRESQL_URL(self) -> SecretStr:
        """Адрес подключения к PostgreSQL

        Адрес подключения к PostgreSQL, собирается при старте сервера

        Args:
            self (Self@Settings): Экземпляр класса Settings

        Returns:
            SecretStr: Полная строка подключения к БД формата 
                'postgresql+asyncpg://username:password@host:port/db_name'

        Raises:
            Exception: В непредвиденной ситуации
        """

        try:
            return SecretStr(
                f"postgresql+asyncpg://"
                f"{self.POSTGRESQL_USER}:{self.POSTGRESQL_PASSWORD.get_secret_value()}"
                f"@{self.POSTGRESQL_HOST}:{self.POSTGRESQL_PORT}"
                f"/{self.POSTGRESQL_DB}"
            )
        except Exception as e:
            desc = f"При сборке адреса подключения к БД произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    class Config:
        """Класс дополнительных настроек

        Класс с дополнительными настройками для класса Settings

        Attributes:
            env_file (str): Название файла с переменными окружения
            env_file_encoding (str): Кодировка файла с переменными окружения
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()