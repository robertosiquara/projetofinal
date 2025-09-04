from sqlalchemy.orm import Session
from backend.models import User, Resource, Request, Alert, CrimeStat
from passlib.context import CryptContext 
from datetime import datetime, timedelta
from jose import jwt
from backend import schemas

# Definir o algoritimo  de hashing
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
#Chave secreta para o token
SECRET_KEY = 'uma_chave_super_secreta'
#Define o algorito de assinatura 
ALGORITHM = 'HS256'
#Define o tempo de expiração do token
ACCESS_TOKEN_EXPIRE_MINUTES = 120

#Função para buscar usuário
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

#Função para criar um novo usuário
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(name= user.name, username= user.username, hashed_password= hashed_password, role= user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Função de autenticação do usuario
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

#Função para criar um TOKEN de autenticação
def create_access_token (data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_resource(db: Session, resource: schemas.ResourceBase, user_id: int):
    print("Dados recebidos no backend:", resource.dict())
    db_resource = Resource(**resource.dict(), registered_by=user_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def list_resources(db: Session):
    # Faz o join e pega o nome do user
    resources = db.query(
        Resource,
        User.name.label("registered_by_name")
    ).join(User, Resource.registered_by == User.id).all()

    # Transforma em lista de dicts para o Pydantic entender
    result = []
    for resource, registered_by_name in resources:
        res_dict = {
            "id": resource.id,
            "name": resource.name,
            "type": resource.type,
            "quantity": resource.quantity,
            "status": resource.status,
            "registered_by": resource.registered_by,
            "registered_by_name": registered_by_name  # <- nome do user
        }
        result.append(res_dict)

    return result

def get_resources(db: Session):
    return db.query(Resource).all()

def update_resource(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource:
        for key,  value in resource.dict(exclude_unset=True).items():
           setattr(db_resource, key, value)
        db.commit()
        db.refresh(db_resource)
    return db_resource 

def delete_resource(db: Session, resource_id: int):
    db_resource =  db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource:
        db.delete(db_resource)
        db.commit()
    return db_resource

def create_request(db: Session, request: schemas.RequestCreate, user_id: int):
    db_request = Request(**request.dict(), requested_by= user_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return(db_request)

def get_requests(db: Session):
    return db.query(Request).all()

def list_requests(db: Session):
    requests = db.query(
        Request,
        User.name.label("requested_by_name"),
        User.id.label("requested_by_id"),
        User.name.label("status_changed_by_name")
    ).join(User, Request.requested_by == User.id).outerjoin(User, Request.status_changed_by == User.id).all()
    result = []
    for request, requested_by_name, requested_by_id, status_changed_by_name in requests:
        req_dict = {
            "id": request.id,
            "equipment_name": request.equipment_name,
            "quantity": request.quantity,
            "status": request.status,
            "requested_by": request.requested_by,
            "requested_by_name": requested_by_name,
            "requested_by_id": requested_by_id,
            "status_changed_by": request.status_changed_by,
            "status_changed_by_name": status_changed_by_name
        }
        result.append(req_dict)
    return result

def update_request(db: Session, request_id: int, status: str | None = None, quantity: int | None = None, status_changed_by: int | None = None):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        return None
    
    if quantity is not None:
        db_request.quantity = quantity
    if status is not None:
        db_request.status = status
    if status_changed_by is not None:
        db_request.status_changed_by = status_changed_by

    db.commit()
    db.refresh(db_request)
    return db_request

def get_crime_stats(db: Session):
    return db.query(CrimeStat).all()

# Alerts fictícios
def get_alerts(db: Session):
    return db.query(Alert).all()


