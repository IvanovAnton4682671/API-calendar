from core.logger import setup_logger
from core.consts import DAY_TYPES, WEEK_DAYS
from pydantic import BaseModel, Field, field_validator
import datetime
from typing import Optional
from fastapi import HTTPException, status

logger = setup_logger("schemas")

def validate_type_text(type_text: str) -> str:
    """Валидация поля type_text

    Валидация поля type_text; поле должно принимать значения из константы DAY_TYPES
    Функция предназначена для использоваться как валидатор в классе Pydantic

    Args:
        type_text (str): Описание типа дня

    Returns:
        str: Описание типа дня, если оно прошло валидацию

    Raises:
        ValueError: При некорректном значении type_text
        Exception: В непредвиденной ситуации

    Examples:
        >>>class Test(BaseModel):
        >>>type_text: str = Filed(...)
        >>>_validate_type_text = field_validator("type_text")(validate_type_text)
    """

    try:
        vars = DAY_TYPES.values()
        if type_text not in vars:
            desc = f"Поле type_text может принимать значения {vars}, но принимает значение {type_text}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        return type_text
    except Exception as e:
        desc = f"При валидации поля type_text={type_text} произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

def validate_week_day(week_day: str) -> str:
    """Валидация поля week_day

    Валидация поля week_day; поле должно принимать значения из константы WEEK_DAYS
    Функция предназначена для использоваться как валидатор в классе Pydantic

    Args:
        week_day (str): Сокращённое наименование дня

    Returns:
        str: Сокращённое наименование дня, если оно прошло валидацию

    Raises:
        ValueError: При некорректном значении week_day
        Exception: В непредвиденной ситуации

    Examples:
        >>>class Test(BaseModel):
        >>>week_day: str = Filed(...)
        >>>_validate_week_day = field_validator("week_day")(validate_week_day)
    """

    try:
        vars = WEEK_DAYS
        if week_day not in vars:
            desc = f"Поле week_day может принимать значения {vars}, но принимает значение {week_day}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        return week_day
    except Exception as e:
        desc = f"При валидации поля week_day={week_day} произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

class BaseCalendarDay(BaseModel):
    """Схема обычного календарного дня

    Класс описывает схему валидации данных для обычного календарного дня

    Attributes:
        date (datetime.date): Дата дня
        type_id (int): Id типа дня
        type_text (str): Описание типа дня
        week_day (str): Сокращённое наименование дня
        _validate_type_text (@field_validator): Валидатор поля type_text
        _validate_week_day (@field_validator): Валидатор поля week_day

    Examples:
        >>>base_day = BaseCalendarDay(date=...,...)
    """

    date: datetime.date = Field(
        ...,
        description="Дата дня"
    )
    type_id: int = Field(
        ...,
        ge=1,
        le=3,
        description="Id типа дня"
    )
    type_text: str = Field(
        ...,
        min_length=12,
        max_length=24,
        description="Описание типа дня"
    )
    week_day: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Сокращённое наименование дня"
    )

    _validate_type_text = field_validator("type_text")(validate_type_text)
    _validate_week_day = field_validator("week_day")(validate_week_day)

    class Config:
        """Класс дополнительных настроек

        Класс с дополнительными настройками для класса BaseCalendarDay

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True

class CalendarDayInput(BaseModel):
    """Схема данных для создания календарного дня

    Класс описывает схему валидации данных для создания календарного дня

    Attributes:
        date (datetime.date): Дата дня
        type_id (int): Id типа дня

    Examples:
        >>>input_data = CalendarDayInput(data=...,...)
    """

    date: datetime.date = Field(
        ...,
        description="Дата дня"
    )
    type_id: int = Field(
        ...,
        ge=1,
        le=3,
        description="Id типа дня"
    )

    class Config:
        """Класс дополнительных настроек

        Класс с дополнительными настройками для класса CalendarDayInput

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True

class CalendarDayInDB(BaseModel):
    """Схема календарного дня в БД

    Класс описывает схему валидации данных для календарного дня в БД

    Attributes:
        id (int): Id дня
        date (datetime.date): Дата дня
        type_id (int): Id типа дня
        type_text (str): Описание типа дня
        note (str): Дополнительное описание дня
        week_day (str): Сокращённое наименование дня
        _validate_type_text (@field_validator): Валидатор поля type_text
        _validate_week_day (@field_validator): Валидатор поля week_day
    """

    id: int = Field(
        ...,
        description="Id дня"
    )
    date: datetime.date = Field(
        ...,
        description="Дата дня"
    )
    type_id: int = Field(
        ...,
        ge=1,
        le=3,
        description="Id типа дня"
    )
    type_text: str = Field(
        ...,
        min_length=12,
        max_length=24,
        description="Описание типа дня"
    )
    note: Optional[str] = Field(
        None,
        max_length=255,
        description="Дополнительное описание дня"
    )
    week_day: str = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Сокращённое наименование дня"
    )

    _validate_type_text = field_validator("type_text")(validate_type_text)
    _validate_week_day = field_validator("week_day")(validate_week_day)

    class Config:
        """Класс дополнительных настроек

        Класс с дополнительными настройками для класса CalendarDayInDB

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True