from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend import auth, crud, database, schemas

router = APIRouter()

@router.get('/stats', response_model= list[schemas.CrimeStat])
def get_stats(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_employee_or_higher)):
    return crud.get_crime_stats(db)