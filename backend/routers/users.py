from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend import crud, models, schemas, database, auth

router = APIRouter()

#rotas referente aos usuários
@router.post('/token')
def login_for_acess_token( form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Login ou senha incorreto.')
    access_token = crud.create_access_token(data={'sub': user.username,"name": user.name, 'role': user.role})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.post('/', response_model= schemas.User)
def create_user(user: schemas.UserCreate, db: Session =  Depends(database.get_db), current_user:schemas.User= Depends(auth.get_current_manager_or_admin)):
    db_user = crud.get_user(db, username= user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.get('/', response_model= list[schemas.User])
def read_users(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_manager_or_admin)):
    return db.query(models.User).all()

@router.put('/{user_id}',  response_model= schemas.User)
def update_user(user_id: int, db: Session = Depends(database.get_db), user: schemas.User = Depends(auth.get_current_manager_or_admin)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado.')
    db_user.name = user.name
    db_user.username = user.username
    db_user.hashed_password = crud.pwd_context.hash(user.password)
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(database.get_db), current_user: schemas.User= Depends(auth.get_current_manager_or_admin)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='Usuário não encontrado.')
    db.delete(db_user)
    db.commit()
    return{"detail": "Usuário deletado"}