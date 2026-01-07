from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from backend import schemas, crud, database, auth

router = APIRouter()

@router.post('/', response_model= schemas.ResourceSchema)
def create_resource(resource:schemas.ResourceBase, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)):
    return crud.create_resource(db, resource, current_user.id)

@router.get('/', response_model= list[schemas.ResourceSchema])
def read_resources(db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)):
    return crud.get_resources(db)

@router.put('/{resource_id}', response_model= schemas.ResourceSchema)
def update_resource(resource_id: int, resource: schemas.ResourceSchema, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)):
    db_resource =  crud.update_resource(db, resource_id, resource)
    if not db_resource:
        raise HTTPException(status_code= 404, detail= 'Resourse não encontrado.')
    return db_resource

@router.delete('/{resource_id}')
def delete_resource(resource_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)):
    db_delete_resource = crud.delete_resource(db, resource_id)
    if not db_delete_resource:
        raise HTTPException(status_code= 404, detail= 'Resource não encontrado.')
    return {'Detail': 'Recurso deletado.'}