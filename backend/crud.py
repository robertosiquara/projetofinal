from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from backend.models import User, Resource, Request, Alert, CrimeStat
from passlib.context import CryptContext 
from datetime import datetime, timedelta, timezone
from jose import jwt
from backend import schemas
from typing import  Optional

# Definir o algoritimo de hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# Chave secreta para o token
SECRET_KEY = 'uma_chave_super_secreta'
# Define o algorito de assinatura 
ALGORITHM = 'HS256'
# Define o tempo de expiração do token
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# --- Funções de Autenticação ---

# Função para buscar usuário

def get_user(db: Session, username: str):
    stmt = select(User).where(User.username == username)
    return db.scalars(stmt).first()

# Função para criar um novo usuário (Permanece a mesma, pois é ORM padrão)
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.name, 
        username=user.username, 
        hashed_password=hashed_password, 
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Função para editar usuários 
def update_user(db:Session, user_id : int, name: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None, role: Optional[str] = None):
    hashed_password = pwd_context.hash(password)
    db_user = db.scalars(select(User).where(User.id == user_id)).first()

    if not db_user:
        return None
    if name is not None:
        db_user.name = name
    if username is not None:
        db_user.username = username
    if password is not None:
        db_user.hashed_password = hashed_password
    if role is not None:
        db_user.role = role
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id: int):
    db_user = db.scalars(select(User).where(User.id == user_id)).first()

    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Função de autenticação do usuario (Nenhuma mudança necessária, usa get_user)
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

# Função para criar um TOKEN de autenticação (Nenhuma mudança, não usa SQLAlchemy)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + (expires_delta or timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire}) 
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM) 

# Função para criar um novo recurso (Nenhuma mudança, é ORM padrão)
def create_resource(db: Session, resource: schemas.ResourceCreate, user_id: int):
    db_resource = Resource(**resource.dict(), registered_by = user_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Função para listar recursos (JOIN complexo - requer .execute)
def list_resources(db: Session):
    stmt = (
        select(
            Resource,
            User.name.label("registered_by_name")
        )
        .join(User, Resource.registered_by == User.id)
    )
    resources = db.execute(stmt).all()

    result = []
    for resource, registered_by_name in resources:
        res_dict = {
            'id': resource.id,
            'name': resource.name,
            'type': resource.type,
            'quantity': resource.quantity,
            'status': resource.status,
            'registered_by': resource.registered_by,
            'registered_by_name': registered_by_name
        }
        result.append(res_dict)
    return result

def get_resources(db: Session):
    stmt = select(Resource)
    return db.scalars(stmt).all()

# Função para editar recurso selecionado (Permanece a mesma, usa busca 1.x)
def update_resource(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.scalars(select(Resource).where(Resource.id == resource_id)).first()

    if db_resource:
        for key, value in resource.dict(exclude_unset = True).items():
            setattr(db_resource, key, value)
            
        db.commit()
        db.refresh(db_resource)
        return db_resource
# Função para deletar recurso selecionado
def delete_resource(db: Session, resource_id: int):
    db_resource = db.scalars(select(Resource).where(Resource.id == resource_id)).first()
        
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource

# --- Funções de CRUD de Solicitação (Request) ---

# Função para criar solicitação (Nenhuma mudança, é ORM padrão)
def create_request(db: Session, request: schemas.RequestCreate, user_id: int):
    db_request = Request(**request.dict(), requested_by=user_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

# Função para listar solicitações (simples)
def get_requests(db: Session):
    return db.scalars(select(Request)).all()

# Função para listar solicitações trazendo o nome de quem criou e de quem mudou o status
def list_requests(db: Session):
    RequestedByUser = aliased(User)
    StatusChangedByUser = aliased(User)

    stmt = select(
        Request,
        RequestedByUser.name.label("requested_by_name"),
        StatusChangedByUser.name.label("status_changed_by_name")
    ).join(
        RequestedByUser, Request.requested_by == RequestedByUser.id
    ).outerjoin(
        StatusChangedByUser, Request.status_changed_by == StatusChangedByUser.id
    )

    requests = db.execute(stmt).all()

    result = []
    # O resultado são tuplas (Request_objeto, requested_name, requested_id, status_name)
    for request, requested_by_name,  status_changed_by_name in requests:
        req_dict = {
            "id": request.id,
            "equipment_name": request.equipment_name,
            "quantity": request.quantity,
            "status": request.status,
            "requested_by": request.requested_by,
            "requested_by_name": requested_by_name,
            "status_changed_by": request.status_changed_by, 
            "status_changed_by_name": status_changed_by_name
        }
        result.append(req_dict)
    return result

# Função para editar solicitação selecionada
def update_request(
    db: Session, 
    request_id: int, 
    status: Optional[str] = None, 
    quantity: Optional[int] = None, 
    status_changed_by: Optional[int] = None
):

    db_request = db.scalars(select(Request).filter(Request.id == request_id)).first()
    
    if not db_request:
        return None
    
    if quantity is not None:
        db_request.quantity = quantity
    if status is not None:
        db_request.status = status
    if status_changed_by is not None:
        db_request.status_changed_by= status_changed_by 

    db.commit()
    db.refresh(db_request)
    return db_request

# --- Funções de Consulta de Estatísticas ---

# Função para listar crimes 
def get_crime_stats(db: Session):
    return db.scalars(select(CrimeStat)).all()

# Função para listar Alertas fictícios
def get_alerts(db: Session):
    return db.scalars(select(Alert)).all()