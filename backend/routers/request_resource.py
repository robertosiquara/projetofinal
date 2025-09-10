from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import auth, schemas, database, crud

router = APIRouter()

#rotas referente às solicitações de recursos
@router.post('/', response_model= schemas.Request)
def create_request(request: schemas.RequestBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_manager_or_admin)):
    return crud.create_request(db, request, current_user.id)