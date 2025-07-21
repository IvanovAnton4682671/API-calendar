from fastapi import Header, HTTPException, status
from core.config import settings

def verify_auth(authentication: str = Header(...)) -> None:
    """Проверяет корректность токена доступа

    Получает от пользователя токен доступа в заголовке запроса, и если он корректен - разрешает дальнейшее взаимодействие
    Предполагается использование как зависимость в защищённых запросах

    Args:
        authorization (str): Заголовок с токеном

    Example:
        >>>@app.post("/db/post", dependencies=[Depends(verify_auth)])
    """

    authentication_list = authentication.split(" ")
    if not authentication.startswith("Bearer ") or len(authentication_list) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный формат токена доступа! Используйте Bearer токен"
        )
    else:
        print(authentication_list)
        token = authentication_list[1]
        print(token)
        if token != settings.API_TOKEN.get_secret_value():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Неверный токен доступа!"
            )