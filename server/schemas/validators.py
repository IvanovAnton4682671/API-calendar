from core.logger import setup_logger
from core.consts import DAY_TYPES, WEEK_DAYS, PERIOD_TYPES
import datetime
from fastapi import HTTPException, status

logger = setup_logger("schemas.validators")

def validate_type_text(type_text: str) -> str:
    """Валидация поля type_text

    Валидация поля type_text; поле должно принимать значения из константы DAY_TYPES
    Функция предназначена для использоваться как валидатор в классе Pydantic

    Args:
        type_text (str): Описание типа дня

    Returns:
        str: Описание типа дня, если оно прошло валидацию

    Raises:
        HTTPException: В непредвиденной ситуации

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
        HTTPException: В непредвиденной ситуации

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
        HTTPException: В непредвиденной ситуации

    Examples:
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
        HTTPException: В непредвиденной ситуации

    Examples:
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
        HTTPException: В непредвиденной ситуации

    Examples:
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