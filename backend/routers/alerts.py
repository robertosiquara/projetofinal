from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend import auth, crud, schemas, database

router = APIRouter()

@router.get('/', response_model= list[schemas.AlertSchema])
def get_alerts(db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_admin)):
    return crud.get_alerts(db)