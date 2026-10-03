from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .errors import InvalidCredentialsError
from .service import autenticar

bearer = HTTPBearer(auto_error=False)


def session_token(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Inicia sesión para continuar.", headers={"WWW-Authenticate": "Bearer"})
    return credentials.credentials


def usuario_actual(token: Annotated[str, Depends(session_token)]) -> dict:
    try:
        return autenticar(token)
    except InvalidCredentialsError as error:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(error), headers={"WWW-Authenticate": "Bearer"}) from error


UsuarioActual = Annotated[dict, Depends(usuario_actual)]


def moderador_actual(user: UsuarioActual) -> dict:
    if not user["es_admin"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Esta acción requiere moderación.")
    return user


ModeradorActual = Annotated[dict, Depends(moderador_actual)]
