from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend import auth, crud, schemas
from backend.database import get_db
from backend.models import RequestStatusEnum, RoleEnum, User

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(auth.get_current_authenticated_user)]
CurrentManager = Annotated[User, Depends(auth.get_current_manager_or_admin)]


@router.post("/", response_model=schemas.RequestOut, status_code=status.HTTP_201_CREATED)
def create_request(payload: schemas.RequestCreate, db: DatabaseSession, current: CurrentUser):
    request = crud.create_request(db, payload, current.id)
    return {**schemas.RequestOut.model_validate(request).model_dump(), "requested_by_name": current.name}


@router.get("/", response_model=list[schemas.RequestOut])
def read_requests(
    db: DatabaseSession,
    current: CurrentUser,
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return crud.list_requests(db, current, limit, offset)


@router.patch("/{request_id}/quantity", response_model=schemas.RequestOut)
def update_request_quantity(
    request_id: int,
    payload: schemas.RequestQuantityUpdate,
    db: DatabaseSession,
    current: CurrentUser,
):
    request = crud.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    if request.status != RequestStatusEnum.PENDING:
        raise HTTPException(status_code=409, detail="Somente solicitações pendentes podem ser alteradas.")
    if current.role == RoleEnum.EMPLOYEE and request.requested_by != current.id:
        raise HTTPException(status_code=403, detail="Você só pode alterar suas próprias solicitações.")
    updated = crud.update_request_quantity(db, request, payload.quantity)
    return {**schemas.RequestOut.model_validate(updated).model_dump(), "requested_by_name": updated.requested_by_user.name}


@router.patch("/{request_id}/status", response_model=schemas.RequestOut)
def update_request_status(
    request_id: int,
    payload: schemas.RequestStatusUpdate,
    db: DatabaseSession,
    current: CurrentManager,
):
    request = crud.get_request(db, request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    if request.status != RequestStatusEnum.PENDING:
        raise HTTPException(status_code=409, detail="Esta solicitação já foi encerrada.")
    updated = crud.update_request_status(db, request, payload.status, current.id)
    return {
        **schemas.RequestOut.model_validate(updated).model_dump(),
        "requested_by_name": updated.requested_by_user.name,
        "status_changed_by_name": current.name,
    }
