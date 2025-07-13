from core.logger import setup_logger
from pydantic import BaseModel, Field, field_validator
import datetime
from typing import Optional
from core.consts import DAY_TYPES, WEEK_DAYS

logger = setup_logger("schemas.calendar_day")

def validate_type_text(type_text: str) -> str:
    """
    ### Валидация поля type_text
    """

    try:
        vars = DAY_TYPES.values()
        if type_text not in vars:
            desc = f"Поле type_text может принимать значения {vars}, но получено значение {type_text}"
            logger.warning(desc)
            raise ValueError(desc)
        return type_text
    except Exception as e:
        desc = f"При валидации поля type_text произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

def validate_week_day(week_day: str) -> str:
    """
    ### Валидация поля week_day
    """

    try:
        vars = WEEK_DAYS
        if week_day not in vars:
            desc = f"Поле week_day может принимать значения {vars}, но получено значение {week_day}"
            logger.warning(desc)
            raise ValueError(desc)
        return week_day
    except Exception as e:
        desc = f"При валидации поля week_day произошла ошибка: {str(e)}"
        logger.error(desc, exc_info=True)
        raise Exception(desc)

class BaseCalendarDay(BaseModel):
    """
    ### Представление обычного календарного дня
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
        from_attributes = True

class CalendarDayInput(BaseModel):
    """
    ### Представление получаемых данных для создания календарного дня
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
        from_attributes = True

class CalendarDayInDB(BaseModel):
    """
    ### Представление календарного дня в БД
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
        from_attributes = True