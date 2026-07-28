from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from backend import auth, crud, schemas
from backend.database import get_db
from backend.models import User

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentManager = Annotated[User, Depends(auth.get_current_manager_or_admin)]
CurrentUser = Annotated[User, Depends(auth.get_current_authenticated_user)]


@router.post("/", response_model=schemas.ResourceOut, status_code=status.HTTP_201_CREATED)
def create_resource(payload: schemas.ResourceCreate, db: DatabaseSession, current: CurrentManager):
    resource = crud.create_resource(db, payload, current.id)
    return {**schemas.ResourceOut.model_validate(resource).model_dump(), "registered_by_name": current.name}


@router.get("/", response_model=list[schemas.ResourceOut])
def read_resources(
    db: DatabaseSession,
    _current: CurrentUser,
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return crud.list_resources(db, limit, offset)


@router.patch("/{resource_id}", response_model=schemas.ResourceOut)
def update_resource(resource_id: int, payload: schemas.ResourceUpdate, db: DatabaseSession, _current: CurrentManager):
    resource = crud.get_resource(db, resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado.")
    updated = crud.update_resource(db, resource, payload)
    return {**schemas.ResourceOut.model_validate(updated).model_dump(), "registered_by_name": updated.registered_by_user.name}


@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: DatabaseSession, _current: CurrentManager) -> Response:
    resource = crud.get_resource(db, resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado.")
    crud.delete_resource(db, resource)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
