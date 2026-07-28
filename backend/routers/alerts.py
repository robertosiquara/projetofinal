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


@router.get("/", response_model=list[schemas.AlertOut])
def read_alerts(db: DatabaseSession, _current: CurrentManagerOrAdmin):
    return crud.get_alerts(db)
