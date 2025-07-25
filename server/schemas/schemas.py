from core.logger import setup_logger
from pydantic import BaseModel, Field, field_validator
import datetime
from typing import Optional
from schemas.validators import validate_type_text, validate_week_day, validate_date, validate_work_week_type, validate_period

logger = setup_logger("schemas.schemas")

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

        Класс дополнительных настроек

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

        Класс дополнительных настроек

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

    Examples:
        >>>calendar_day_in_db = CalendarDayInDB(cdidb).model_validate()
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

        Класс дополнительных настроек

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True

class ReadyCalendarDay(BaseModel):
    """Схема готового календарного дня

    Класс описывает схему валидации данных для готового календарного дня

    Attributes:
        date (str): Дата дня формата ДД.ММ.ГГГГ
        type_id (int): Id типа дня
        type_text (str): Описание типа дня
        note (Optional[str]): Дополнительное описание дня
        week_day (str): Сокращённое наименование дня
        _validate_type_text (@field_validator): Валидатор поля type_text
        _validate_week_day (@field_validator): Валидатор поля week_day

    Examples:
        >>>ready_calendar_day = ReadyCalendarDay(date=...,...)
    """

    date: str = Field(
        ...,
        min_length=10,
        max_length=10,
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

        Класс дополнительных настроек

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True

class ProductionCalendar(BaseModel):
    """Схема производственного календаря

    Класс описывает схему валидации данных производственного календаря

    Attributes:
        date_start (str): Дата первого дня в календаре
        date_end (str): Дата последнего дня в календаре
        work_week_type (str): Тип рабочей недели
        period (str): Тип периода
        calendar_days (Optional[int]): Кол-во календарных дней
        calendar_days_without_holidays (Optional[int]): Кол-во календарных дней без праздников
        work_days (Optional[int]): Кол-во рабочих дней
        weekends (Optional[int]): Кол-во выходных дней
        holidays (Optional[int]): Кол-во праздничных дней
        days (list[ReadyCalendarDay]): Список готовых дней
        _validate_date_start (@field_validator): Валидатор поля date_start
        _validate_date_end (@field_validator): Валидатор поля date_end
        _validate_work_week_type (@field_validator): Валидатор поля work_week_type
        _validate_period (@field_validator): Валидатор поля period

    Examples:
        >>>production_calendar = ProductionCalendar(date_start=...,...)
    """

    date_start: str = Field(
        ...,
        min_length=10,
        max_length=10,
        description="Дата первого дня в календаре"
    )
    date_end: str = Field(
        ...,
        min_length=10,
        max_length=10,
        description="Дата последнего дня в календаре"
    )
    work_week_type: str = Field(
        ...,
        min_length=24,
        max_length=24,
        description="Тип рабочей недели"
    )
    period: str = Field(
        ...,
        min_length=3,
        max_length=19,
        description="Тип периода"
    )
    calendar_days: Optional[int] = Field(
        None,
        ge=0,
        description="Кол-во календарных дней"
    )
    calendar_days_without_holidays: Optional[int] = Field(
        None,
        ge=0,
        description="Кол-во календарных дней без праздников"
    )
    work_days: Optional[int] = Field(
        None,
        ge=0,
        description="Кол-во рабочих дней"
    )
    weekends: Optional[int] = Field(
        None,
        ge=0,
        description="Кол-во выходных дней"
    )
    holidays: Optional[int] = Field(
        None,
        ge=0,
        description="Кол-во праздничных дней"
    )
    days: list[ReadyCalendarDay] = Field(
        ...,
        description="Список готовых дней"
    )

    _validate_date_start = field_validator("date_start")(validate_date)
    _validate_date_end = field_validator("date_end")(validate_date)
    _validate_work_week_type = field_validator("work_week_type")(validate_work_week_type)
    _validate_period = field_validator("period")(validate_period)

    class Config:
        """Класс дополнительных настроек

        Класс дополнительных настроек

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True