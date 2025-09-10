from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import auth, crud, database, schemas

router = APIRouter()

#rotas referente aos alertas
@router.get('/', response_model= list[schemas.Alert])
def get_alerts(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.get_alerts(db)