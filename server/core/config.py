from core.logger import setup_logger
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr, computed_field, model_validator

logger = setup_logger("core.config")

class Settings(BaseSettings):
    """
    ### Описывает все используемые переменные окружения
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

    @computed_field
    @property
    def POSTGRESQL_URL(self) -> SecretStr:
        """
        ### Адрес подключения к PostgreSQL, собирается при старте сервера
        """

        return SecretStr(
            f"postgresql+asyncpg://"
            f"{self.POSTGRESQL_USER}:{self.POSTGRESQL_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRESQL_HOST}:{self.POSTGRESQL_PORT}"
            f"/{self.POSTGRESQL_DB}"
        )

    @model_validator(mode="after")
    def validate_url(self) -> "Settings":
        """
        ### Проверяет наличие адреса подключения к PostgreSQL
        """

        try:
            if not self.POSTGRESQL_URL.get_secret_value():
                desc = f"Некорректные данные адреса подключения к PostgreSQL: {self.POSTGRESQL_URL.get_secret_value()}"
                logger.warning(desc)
                raise ValueError(desc)
            return self
        except Exception as e:
            logger.error(f"При проверке POSTGRESQL_URL произошла ошибка: {str(e)}", exc_info=True)
            raise

    class Config:
        """
        ### Описывает используемый `.env`-файл
        """

        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()