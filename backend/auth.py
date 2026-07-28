from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend import crud
from backend.config import settings
from backend.database import get_db
from backend.models import RoleEnum, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")
DatabaseSession = Annotated[Session, Depends(get_db)]
AccessToken = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: DatabaseSession, token: AccessToken) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou expiradas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = int(payload.get("sub", ""))
    except (JWTError, TypeError, ValueError) as exc:
        raise unauthorized from exc

    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise unauthorized

    return user


def require_roles(*roles: RoleEnum) -> Callable[..., User]:
    def dependency(user: Annotated[User, Depends(get_current_user)]) -> User:
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não possui permissão para esta operação.",
            )
        return user

    return dependency


get_current_admin = require_roles(RoleEnum.ADMIN)
get_current_manager_or_admin = require_roles(RoleEnum.ADMIN, RoleEnum.MANAGER)
get_current_authenticated_user = require_roles(
    RoleEnum.ADMIN,
    RoleEnum.MANAGER,
    RoleEnum.EMPLOYEE,
)
