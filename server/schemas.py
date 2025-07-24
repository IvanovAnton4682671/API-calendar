from core.logger import setup_logger
from core.consts import DAY_TYPES, WEEK_DAYS, PERIOD_TYPES
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
        if type_text not in DAY_TYPES.values():
            desc = f"Поле type_text может принимать значения {DAY_TYPES.values()}, но принимает значение {type_text}"
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
        if week_day not in WEEK_DAYS:
            desc = f"Поле week_day может принимать значения {WEEK_DAYS}, но принимает значение {week_day}"
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

def validate_date(date: str) -> str:
    """Валидация поля date формата ДД.ММ.ГГГГ

    Валидация поля date (поля date_start, date_end); поле должно принимать формат ДД.ММ.ГГГГ
    Функция предназначена для использования как валидатор в классе Pydantic

    Args:
        date (str): Строковая дата ДД.ММ.ГГГГ

    Returns:
        str: Дата в том же формате, если она прошла валидацию

    Raises:
        HTTPException: в разных случаях

    Example:
        >>>class Test(BaseModel):
        >>>date: str = Filed(...)
        >>>_validate_date = field_validator("date")(validate_date)
    """

    try:
        date_parts = date.split(".")
        if len(date_parts) != 3 or len(date_parts[0]) != 2 or len(date_parts[1]) != 2 or len(date_parts[2]) != 4:
            desc = f"Поле date может принимать значение формата ДД.ММ.ГГГГ, но принимает значение {date}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        try:
            day = int(date_parts[0])
            month = int(date_parts[1])
            year = int(date_parts[2])
        except Exception as e:
            desc = f"Все компоненты даты должны быть числами, однако получено {date}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        datetime.date(year, month, day)
        return date
    except Exception as e:
        desc = f"При валидации поля date={date} произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

def validate_work_week_type(work_week_type: str) -> str:
    """Валидация поля work_week_type

    Валидация поля work_week_type4; должно начинаться с 5 или 6
    Функция предназначена для использования как валидатор в классе Pydantic

    Args:
        work_week_type (str): Тип рабочей недели

    Returns:
        str: Тот же тип рабочей недели, если он прошёл валидацию

    Raises:
        HTTPException: в разных случаях

    Example:
        >>>class Test(BaseModel):
        >>>work_week_type: str = Filed(...)
        >>>_validate_validate_work_week_type = field_validator("validate_work_week_type")(validate_work_week_type)
    """

    try:
        if int(work_week_type[0]) not in (5, 6):
            desc = f"Поле work_week_type может обозначать 5- или 6-дневную рабочую неделю, но получено значение {work_week_type}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        return work_week_type
    except Exception as e:
        desc = f"При валидации поля work_week_type={work_week_type} произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )

def validate_period(period: str) -> str:
    """Валидация поля period

    Валидация поля period; должно принимать значение из константы PERIOD_TYPES
    Функция предназначена для использования как валидатор в классе Pydantic

    Args:
        period (str): Период календаря

    Returns:
        str: Тот же период календаря, если он прошёл валидацию

    Raises:
        HTTPException: в разных случаях

    Example:
        >>>class Test(BaseModel):
        >>>period: str = Filed(...)
        >>>_validate_period = field_validator("period")(validate_period)
    """

    try:
        if period not in PERIOD_TYPES:
            desc = f"Поле period может принимать значения {PERIOD_TYPES}, но принимает значение {period}"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=desc
            )
        return period
    except Exception as e:
        desc = f"При валидации поля period={period} произошла ошибка: {str(e)}"
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

        Класс с дополнительными настройками для класса ReadyCalendarDay

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

        Класс с дополнительными настройками для класса ProductionCalendar

        Attributes:
            from_attributes (bool): Для синхронизации с полями ORM-модели
        """

        from_attributes = True