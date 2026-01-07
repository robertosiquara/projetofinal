from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from backend import auth, schemas, database, crud

router = APIRouter()

@router.get('/', response_model= list[schemas.RequestSchema])
def read_request(db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_employee_or_higher)):
    return crud.get_requests(db)

@router.put('/{request_id}', response_model= schemas.RequestSchema)
def update_request_status(request_id: int, request: schemas.RequestUpdate ,db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_employee_or_higher)):
    db_request = crud.update_request(db, request_id, status= request.status, quantity= request.quantity, status_changed_by= current_user.id)
    if not db_request:
        raise HTTPException(status_code= 404, detail= 'Requisição não encontrada.')
    return db_request