from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend import crud, schemas, database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/token')

def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail='Não consegui validar suas credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str  = payload.get('sub')
        sub: str = payload.get('role')
        if username is None or sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, username= username)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(user: schemas.User = Depends(get_current_user)):
    if user.role != 'Admin':
        raise HTTPException(status_code=403, detail= 'Não possui permissão')
    return user

def get_current_manager_or_admin(user: schemas.User = Depends(get_current_user)):
    if user.role not in ['Admin', 'Gerente']:
        raise HTTPException(status_code= 403, detail='Não possui permissão')
    return user

def get_current_employee_or_higher(user: schemas.User = Depends(get_current_user)):
    if user.role not in ["Funcionário", "Gerente", "Admin"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

def get_current_batman(user: schemas.User = Depends(get_current_user)):
    if user.username != "batman":
        raise HTTPException(status_code=403, detail="Only Batman can access this")
    return user
