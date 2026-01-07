from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend import auth, schemas, database, crud

router = APIRouter()

@router.post('/', response_model= schemas.RequestSchema)
def create_request( request: schemas.RequestCreate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)):
    return crud.create_request(db, request, current_user.id)