from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import auth, crud, database, schemas

router = APIRouter()

@router.get('/stats', response_model= list[schemas.CrimeStat])
def get_stats(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.get_crime_stats(db)

@router.get('/resources', response_model= list[schemas.ResourceOut])
def read_sesources(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.list_resources(db)

@router.get('/requests', response_model=list[schemas.RequestOut])
def read_requests(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.list_requests(db)