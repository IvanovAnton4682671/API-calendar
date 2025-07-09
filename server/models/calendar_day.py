from core.logger import setup_logger
from databases.postgresql import Base
from sqlalchemy import Column, Integer, Date, String

logger = setup_logger("models.calendar_day")

class CalendarDay(Base):
    """
    ### Таблица календарных дней
    """

    __tablename__ = "calendar_day"

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
        """
        ### Вывод элемента таблицы в терминал
        """

        calendar_day = (
            f"<Day(id={self.id};date={self.date};type_id={self.type_id};"
            f"type_text={self.type_text};note={self.note};week_day={self.week_day})>"
        )
        logger.info(calendar_day)
        return calendar_day