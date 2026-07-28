from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import auth, crud, schemas
from backend.database import get_db
from backend.models import User

router = APIRouter()
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentManagerOrAdmin = Annotated[
    User,
    Depends(auth.get_current_manager_or_admin),
]


@router.get("/stats", response_model=list[schemas.CrimeStatOut])
def read_stats(db: DatabaseSession, _current: CurrentManagerOrAdmin):
    return crud.get_crime_stats(db)


@router.get("/resources", response_model=list[schemas.ResourceOut])
def read_resources(db: DatabaseSession, _current: CurrentManagerOrAdmin):
    return crud.list_resources(db)


@router.get("/requests", response_model=list[schemas.RequestOut])
def read_requests(db: DatabaseSession, current: CurrentManagerOrAdmin):
    return crud.list_requests(db, current)
