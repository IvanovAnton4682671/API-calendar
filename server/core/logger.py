import logging
from fastapi import HTTPException, status

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str) -> logging.Logger:
    """Создаёт логгер для записи в stdout

    Создаёт логгер со своим именем, который пишет логи всех уровней только в stdout
    Предполагается использование для создания отдельного логгера для каждого файла

    Args:
        name (str): Имя логгера

    Raises:
        HTTPException: В непредвиденной ситуации

    Examples:
        >>>logger = setup_logger("filename")
        >>>logger.info("info")
        >>>`2025-01-01 10:00:00 - INFO - filename - info`
    """

    try:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        return logger
    except Exception as e:
        desc = f"При создании логгера name={name} произошла ошибка: {str(e)}"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=desc
        )