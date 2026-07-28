from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend import auth, crud, schemas
from backend.database import get_db
from backend.models import User
from backend.security import create_access_token

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentAdmin = Annotated[User, Depends(auth.get_current_admin)]
CurrentUser = Annotated[User, Depends(auth.get_current_authenticated_user)]


@router.post("/token", response_model=schemas.Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DatabaseSession,
) -> schemas.Token:
    user = crud.authenticate_user(db, form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schemas.Token(access_token=create_access_token(str(user.id)))


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(current_user: CurrentUser) -> User:
    return current_user


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: DatabaseSession, _current: CurrentAdmin) -> User:
    try:
        return crud.create_user(db, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Nome de usuário já cadastrado.") from exc


@router.get("/", response_model=list[schemas.UserOut])
def read_users(
    db: DatabaseSession,
    _current: CurrentAdmin,
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[User]:
    return crud.list_users(db, limit, offset)


@router.patch("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    payload: schemas.UserUpdate,
    db: DatabaseSession,
    current: CurrentAdmin,
) -> User:
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.id == current.id and payload.role is not None and payload.role != current.role:
        raise HTTPException(status_code=400, detail="Você não pode alterar o próprio papel.")
    try:
        return crud.update_user(db, user, payload)
    except IntegrityError as exc:
        raise HTTPException(status_code=409, detail="Nome de usuário já cadastrado.") from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: DatabaseSession,
    current: CurrentAdmin,
) -> Response:
    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.id == current.id:
        raise HTTPException(status_code=400, detail="Você não pode excluir o próprio usuário.")
    crud.delete_user(db, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
