from core.logger import setup_logger
from pydantic import BaseModel, Field, field_validator
import datetime
from typing import Optional
from core.consts import DAY_TYPES, WEEK_DAYS

logger = setup_logger("schemas.calendar_day")

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

    @field_validator("type_text")
    def validate_type_text(type_text: str) -> Optional[str]:
        """
        ### Валидация поля type_text
        """

        try:
            vars = DAY_TYPES
            if type_text not in vars:
                desc = f"Поле type_text может принимать значения {vars}, но получено {type_text}"
                logger.warning(desc)
                raise ValueError(desc)
            return type_text
        except Exception as e:
            logger.error(f"При валидации поля type_text произошла ошибка: {str(e)}", exc_info=True)
            raise

    @field_validator("week_day")
    def validate_week_day(week_day: str) -> Optional[str]:
        """
        ### Валидация поля week_day
        """

        try:
            vars = WEEK_DAYS
            if week_day not in vars:
                desc = f"Поле week_day может принимать значения {vars}, но получено {week_day}"
                logger.warning(desc)
                raise ValueError(desc)
            return week_day
        except Exception as e:
            logger.error(f"При валидации поля week_day произошла ошибка: {str(e)}", exc_info=True)
            raise

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
    note: Optional[str] = Field(
        None,
        max_length=255,
        description="Дополнительное описание дня"
    )

    class Config:
        from_attributes = True