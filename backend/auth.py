from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from backend import crud, database
from backend.models import User, RoleEnum 
from typing import Annotated, Optional 

# --- Variáveis Inalteradas ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/token')

# --- Funções de Dependência ---

def get_current_user(
    db: Session = Depends(database.get_db), 
    token: str = Depends(oauth2_scheme)
): 
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail='Não consegui validar suas credenciais',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: Optional[str] = payload.get('sub')
        role_value: Optional[str] = payload.get('role') 

        if username is None or role_value is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, username=username) 
    
    if user is None:
        raise credentials_exception
        
    return user

# --- Funções de Autorização (Role-Based Access Control) ---

def get_current_admin(user: Annotated[User, Depends(get_current_user)]):
    
    if not isinstance(user.role, RoleEnum) or user.role.value != RoleEnum.admin.value:
         raise HTTPException(status_code=403, detail='Não possui permissão: Requer Admin')
    return user

def get_current_manager_or_admin(user: Annotated[User, Depends(get_current_user)]):
    required_roles = [RoleEnum.admin.value, RoleEnum.gerente.value]
    
    if not isinstance(user.role, RoleEnum) or user.role.value not in required_roles:
        raise HTTPException(status_code=403, detail='Não possui permissão: Requer Gerente ou Admin')
    return user

def get_current_employee_or_higher(user: Annotated[User, Depends(get_current_user)]):
    required_roles = [RoleEnum.funcionario.value, RoleEnum.gerente.value, RoleEnum.admin.value]
    
    if not isinstance(user.role, RoleEnum) or user.role.value not in required_roles:
        raise HTTPException(status_code=403, detail="Não possui permissão: Requer Funcionário ou superior")
    return user

def get_current_batman(user: Annotated[User, Depends(get_current_user)]):
    if user.username != "batman":
        raise HTTPException(status_code=403, detail="Acesso exclusivo do Batman")
    return user