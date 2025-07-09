## Простенькая документация

#### Основные используемые технологии:

- **Python (v3.11.9)**
- **FastAPI (v0.116.0)**
- **Pydantic (v2.11.7)**
- **SQLAlchemy (v2.0.41)**
- **Uvicorn (v0.35.0)**
- **Asyncpg (v0.30.0)**
- **PostgreSQL (postgres:latest (июль 2025))**
- **Docker Compose (v3.8)**

#### Как работает:

- Запускаем контейнер с PostgreSQL:
```bash
docker-compose up --build -d
```
- Запускаем Python-сервер:
```bash
python main.py
```
- Переходим по адресу `http://localhost:8000/docs` (используем стандартный **Swagger**)
- Тыкаем кнопочки

#### Почему работает:

- `main.py` запускает сервер
- `routers/calendar_day.py` обрабатывает эндпоинты, вызывает методы из сервиса
- `services/calendar_day.py` реализует бизнес-логику, работает с данными, вызывает методы из репозитория
- `repositories/calendar_day.py` реализует CRUD-логику, выполняет запросы к БД
- `models/calendar_day.py` описывает реляционную таблицу данных
- `schemas/calendar_day.py` описывает используемые схемы валидации данных
- `databases/postgresql.py` описывает работу с асинхронными сессиями PostgreSQL
- `core/config.py` описывает использование переменных окружения
- `core/logger.py` реализует консольный логгер
- `core/consts.py` содержит нужные константы