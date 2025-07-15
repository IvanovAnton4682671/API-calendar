from core.logger import setup_logger
from databases.postgresql import Base
from sqlalchemy import Column, Integer, Date, String

logger = setup_logger("models.calendar_day")

class CalendarDay(Base):
    """Описывает таблицу календарных дней

    Класс описывает ORM-модель календарного дня для работы с БД PostgreSQL

    Attributes:
        __tablename__ (str): Название таблицы
        id (Integer): Id дня
        date (Date): Дата дня
        type_id (Integer): Id типа дня
        type_text (String): Описание типа дня
        note (String): Дополнительное описание дня
        week_day (String): Сокращённое наименование дня

    Examples:
        >>>calendar_day = CalendarDay(date=...,...)
    """

    __tablename__: str = "calendar_day"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Id дня"
    )
    date = Column(
        Date,
        nullable=False,
        unique=True,
        comment="Дата дня"
    )
    type_id = Column(
        Integer,
        nullable=False,
        comment="Id типа дня"
    )
    type_text = Column(
        String(24),
        nullable=False,
        comment="Описание типа дня"
    )
    note = Column(
        String(255),
        nullable=True,
        default=None,
        comment="Дополнительное описание дня"
    )
    week_day = Column(
        String(2),
        nullable=False,
        comment="Сокращённое наименование дня"
    )

    def __repr__(self) -> str:
        """Понятно выводит информацию об экземпляре

        Выводит информацию об экземпляре в понятном виде

        Args:
            self (Self@CalendarDay): Экземпляр класса CalendarDay

        Returns:
            str: Строка со всеми полями экземпляра

        Raises:
            Examples: В непредвиденной ситуации

        Examples:
            >>>calendar_day = CalendarDay(date=...,type_id=...,...)
            >>>print(calendar_day)
            >>>`<Day(id=...,...)>`
        """

        return (
            f"<Day(id={self.id};date={self.date};type_id={self.type_id};"
            f"type_text={self.type_text};note={self.note};week_day={self.week_day})>"
        )