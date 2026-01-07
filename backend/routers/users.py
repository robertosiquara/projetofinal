from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional # Importação não estritamente necessária aqui, mas boa prática

# Importações dos módulos backend (ajuste os nomes se necessário)
from backend import crud, models, schemas, database, auth

router = APIRouter()

# --- Rotas de Autenticação ---

@router.post('/token')
def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Login ou senha incorreto.',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = crud.create_access_token(
        data={'sub': user.username, "name": user.name, 'role': user.role}
    )
    
    return {'access_token': access_token, 'token_type': 'bearer'}



## 👥 Rotas de Usuário (CRUD)

@router.post('/', response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user_route(
    user: schemas.UserCreate, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)
):
    
    db_user = crud.get_user(db, username=user.username)
    
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    return crud.create_user(db, user)

@router.get('/', response_model=list[schemas.UserOut])
def read_users(
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)
):
    stmt = select(models.User)
    return db.scalars(stmt).all()

@router.put('/{user_id}', response_model=schemas.UserOut)
def update_user_route(
    user_id: int, 
    user_update: schemas.UserOut, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)
):
    db_user_check = db.scalars(select(models.User).where(models.User.id == user_id)).first()
    if not db_user_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')

    updated_user = crud.update_user(
        db, 
        user_id=user_id, 
        name=user_update.name,
        username=user_update.username,
        password=user_update.password,
        role=user_update.role
    )

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado durante a atualização.')
        
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserOut = Depends(auth.get_current_manager_or_admin)
):
    """
    Deleta um usuário pelo ID. Requer permissão de Gerente ou Administrador.
    Utiliza: crud.delete_user
    """
    # Chama a função delete_user do crud.py
    deleted_user = crud.delete_user(db, user_id)
    
    if not deleted_user:
        # Se a função retornar None, o usuário não foi encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
        
    # Retorna 204 No Content (deleção bem-sucedida sem corpo de resposta)
    return