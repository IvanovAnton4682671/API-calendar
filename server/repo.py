from core.logger import setup_logger
from sqlalchemy.ext.asyncio import AsyncSession
from model import CalendarDay
from typing import Optional
from schemas import CalendarDayInDB
from datetime import date
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

logger = setup_logger("repo")

class CalendarDayRepository:
    """Репозиторий CRUD-логики календарных дней

    Класс описывает основные методы для взаимодействия с БД PostgreSQL, а именно:
    создание дня; получение дней по периоду; обновление дня по дате; удаление дня по дате

    Args:
        session (AsyncSession): Асинхронная сессия для выполнения запросов к БД

    Examples:
        >>>repo = CalendarDayRepository(session)
    """

    def __init__(self, session: AsyncSession) -> None:
        """Конструктор класса

        Создаёт экземпляр класса для работы с асинхронной сессией БД PostgreSQL

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            session (AsyncSession): Асинхронная сессия для выполнения запросов к БД
        """

        self._session = session

    async def create_day(self, day_data: CalendarDay) -> CalendarDayInDB:
        """Создаёт календарный день

        Создаёт календарный день в БД из CalendarDay-модели

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            day_data (CalendarDay): Модель, представляющая все данные для создания календарного дня

        Returns:
            CalendarDayInDB: Представление созданного календарного дня в БД

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>created_day = await repo.create_day(CalendarDay(date=...,...))
        """

        try:
            logger.info(f"Пробуем создать календарный день с данными: {day_data}")
            self._session.add(day_data)
            await self._session.commit()
            await self._session.refresh(day_data)
            logger.info(f"Календарный день успешно создан (перед валидацией): {day_data}")
            return CalendarDayInDB.model_validate(day_data)
        except Exception as e:
            desc = f"При создании календарного дня произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            await self._session.rollback()
            raise Exception(desc)

    async def insert_production_calendar(self, days_list: list[CalendarDay]) -> int:
        """Вставляет производственный календарь

        Вставляет в БД большое количество календарных дней за раз.
        При конфликте (день существует) обновляет поля дня

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            days_list (list[CalendarDay]): Список календарных дней

        Returns:
            int: Кол-во успешных вставок в БД

        Raises:
            Exception: В непредвиденной ситуации

        Example:
            >>>inserted_days = await repo.insert_production_calendar([CalendarDay(...),...])
        """

        try:
            logger.info(f"Пробуем вставить в БД {len(days_list)} календарных дней")
            query = insert(CalendarDay).values([{
                "date": day.date,
                "type_id": day.type_id,
                "type_text": day.type_text,
                "note": day.note,
                "week_day": day.week_day
            } for day in days_list])
            query = query.on_conflict_do_update(index_elements=["date"], set_={
                "type_id": query.excluded.type_id,
                "type_text": query.excluded.type_text,
                "note": query.excluded.note,
                "week_day": query.excluded.week_day
            })
            await self._session.execute(query)
            await self._session.commit()
            inserted = len(days_list)
            logger.info(f"Вставка прошла успешно, было добавлено/обновлено {inserted} календарных дней")
            return inserted
        except Exception as e:
            desc = f"При вставке производственного календаря произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            await self._session.rollback()
            raise Exception(desc)

    async def get_days_by_period(self, date_start: date, date_end: date) -> list[CalendarDayInDB]:
        """Получает календарные дни по периоду

        Получает список календарных дней по периоду с date_start по date_end включительно

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            date_start (date): Дата начала периода
            date_end (date): Дата конца периода

        Returns:
            list[CalendarDayInDB]: Список календарных дней, если такие дни нашлись, иначе пустой список

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>db_days = await repo.get_days_by_period(date(2025, 1, 1), date(2025, 12, 1))
        """

        try:
            logger.info(f"Пробуем получить календарные дни по периоду date_start={date_start}, date_end={date_end}")
            query = select(CalendarDay).where(CalendarDay.date >= date_start, CalendarDay.date <= date_end).order_by(CalendarDay.date)
            result = await self._session.execute(query)
            list_of_days = result.scalars().all()
            if list_of_days:
                logger.info(f"Календарные дни по периоду date_start={date_start}, date_end={date_end} успешно получены, их {len(list_of_days)}")
                return [CalendarDayInDB.model_validate(day) for day in list_of_days]
            else:
                logger.warning(f"Календарные дни по периоду date_start={date_start}, date_end={date_end} отсутствуют")
                return []
        except Exception as e:
            desc = f"При получении календарных дней по периоду date_start={date_start}, date_end={date_end} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    async def get_day_by_date(self, date: date) -> Optional[CalendarDay]:
        """Получает календарный день по дате

        Получает один календарный день по дате date

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            date (date): Дата дня

        Returns:
            Optional[CalendarDay]: Календарный день, если такой день нашёлся, иначе None

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>day = await repo.get_day_by_date(date(2025, 1, 1))
        """

        try:
            logger.info(f"Пробуем получить день date={date}")
            query = select(CalendarDay).where(CalendarDay.date == date)
            result = await self._session.execute(query)
            received_day = result.scalars().first()
            if received_day:
                logger.info(f"Календарный день date={date} успешно получен: {received_day}")
                return received_day
            else:
                logger.warning(f"Календарный день date={date} не существует")
                return None
        except Exception as e:
            desc = f"При получении календарного дня date={date} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            raise Exception(desc)

    async def update_day(self, date: date, day_data: CalendarDay) -> Optional[CalendarDayInDB]:
        """Обновляет календарный день по дате

        Получает календарный день по дате date и обновляет его новыми данными

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            date (date): Дата обновляемого дня
            day_data (CalendarDay): Данные для обновления календарного дня

        Returns:
            Optional[CalendarDayInDB]: Обновлённый календарный день, если такой день существовал, иначе None

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>updated_day = await repo.update_day(date(2025, 1, 1), CalendarDay(date=...,...))
        """

        try:
            logger.info(f"Пробуем обновить календарный день date={date} данными={day_data}")
            received_day = await self.get_day_by_date(date)
            if received_day:
                received_day.date = day_data.date
                received_day.type_id = day_data.type_id
                received_day.type_text = day_data.type_text
                received_day.note = day_data.note
                received_day.week_day = day_data.week_day
                await self._session.commit()
                await self._session.refresh(received_day)
                logger.info(f"Календарный день date={date} успешно обновлён (перед валидацией): {received_day}")
                return CalendarDayInDB.model_validate(received_day)
            else:
                logger.warning(f"Календарный день date={date} не существует")
                return None
        except Exception as e:
            desc = f"При обновлении календарного дня date={date} произошла ошибка: {str(e)}"
            logger.error(desc, exc_info=True)
            await self._session.rollback()
            raise Exception(desc)

    async def delete_day(self, date: date) -> bool:
        """Удаляет календарный день по дате

        Удаляет календарный день по дате date

        Args:
            self (Self@CalendarDayRepository): Экземпляр класса
            date (date): Дата удаляемого дня

        Returns:
            bool: Статус удалённого дня (True - день удалён, False - день не существует)

        Raises:
            Exception: В непредвиденной ситуации

        Examples:
            >>>deleted_day = await repo.delete_day(date(2025, 1, 1))
        """

        try:
            logger.info(f"Пробуем удалить календарный день date={date}")
            calendar_day = await self.get_day_by_date(date)
            if calendar_day:
                await self._session.delete(calendar_day)
                await self._session.commit()
                logger.info(f"Календарный день date={date} успешно удалён")
                return True
            else:
                logger.warning(f"Календарный день date={date} не существует")
                return False
        except Exception as e:
            logger.error(f"При удалении календарного дня произошла ошибка: {str(e)}", exc_info=True)
            await self._session.rollback()
            return False