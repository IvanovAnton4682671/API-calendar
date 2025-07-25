from core.logger import setup_logger
from fastapi import Header, HTTPException, status
from core.config import settings

logger = setup_logger("security")

def verify_auth(authentication: str = Header(...)) -> None:
    """Проверяет корректность токена доступа

    Получает от пользователя токен доступа в заголовке запроса, и если он корректен - разрешает дальнейшее взаимодействие
    Предполагается использование как зависимость в защищённых запросах

    Args:
        authorization (str): Заголовок с токеном

    Raises:
        HTTPException: В непредвиденной ситуации

    Examples:
        >>>@app.post("/db/post", dependencies=[Depends(verify_auth)])
    """

    authentication_list = authentication.split(" ")
    if not authentication.startswith("Bearer ") or len(authentication_list) != 2:
        desc = "Неверный формат токена доступа! Используйте Bearer токен"
        logger.warning(desc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=desc
        )
    else:
        print(authentication_list)
        token = authentication_list[1]
        print(token)
        if token != settings.API_TOKEN.get_secret_value():
            desc = "Неверный токен доступа!"
            logger.warning(desc)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=desc
            )