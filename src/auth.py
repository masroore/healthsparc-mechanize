import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

_AUTH_USER: str | None = None
_AUTH_PASS: str | None = None


def set_credentials(username: str, password: str):
    global _AUTH_USER, _AUTH_PASS
    _AUTH_USER = username
    _AUTH_PASS = password


def get_username() -> str | None:
    return _AUTH_USER


security = HTTPBasic()


async def authenticate(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
) -> str:
    """Authenticate a FastAPI request with HTTP Basic auth."""
    basic_auth_username = _AUTH_USER
    basic_auth_password = _AUTH_PASS
    if not (basic_auth_username and basic_auth_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Server HTTP Basic auth credentials not set",
            headers={"WWW-Authenticate": "Basic"},
        )

    correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), basic_auth_username.encode("utf8")
    )
    correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), basic_auth_password.encode("utf8")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
