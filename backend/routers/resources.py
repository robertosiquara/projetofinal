from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import crud, schemas, database, auth

router = APIRouter()

@router.post('/', response_model= schemas.Resource)
def create_resource(resource: schemas.ResourceBase, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.create_resource(db, resource)

@router.get('/', response_model= list[schemas.Resource])
def read_sesources(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.get_resources(db)

@router.put('/{resource_id}', response_model= schemas.Resource)
def update_resource(resource_id: int, resource: schemas.Resource, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    db_resource = crud.update_resource(db, resource_id, resource)
    if not db_resource:
        raise HTTPException(status_code=404, detail='Recurso não encontrado.' )
    return db_resource

@router.delete('/{resource_id}')
def delete_resource(resource_id: int, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    db_resource = crud.delete_resource(db, resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail='Recurso não encontrado.')
    return{'Detail': 'Recurso delatado.'}