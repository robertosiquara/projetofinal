from pydantic import BaseModel, Field
from backend.models import RoleEnum, TypeEnum
from datetime import date
from typing import Optional


#Validação User
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    role: RoleEnum
    model_config = {
        "use_enum_values": True
    }

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True,
        "use_enum_values": True # Repetido para garantir consistência
    }

#Validação Resource
class ResourceBase(BaseModel):
    name: str
    type: TypeEnum
    quantity: int
    status: Optional[str] = None

    model_config = {
        "use_enum_values": True
    }
        
class ResourceCreate(ResourceBase):
    pass

class ResourceOut(BaseModel):
    id: int
    name: str
    type: str
    quantity: int
    status: str
    registered_by: int
    registered_by_name: str  
    
    model_config = {
        "from_attributes": True
    }


class ResourceSchema(ResourceBase):
    id: int


    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[TypeEnum] = None
    quantity: Optional[int] = None  
    status: Optional[str] = None

    model_config = {
        "use_enum_values": True
    }

#Validação Request
class RequestBase(BaseModel):
    equipment_name: str
    status: Optional[str] = "Pendente"

class RequestCreate(RequestBase):
    quantity: Optional[int] = None 

class RequestUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = 'Concluído'

class RequestSchema(RequestBase):
    id: int
    requested_by: int
    status_changed_by: Optional[int] = None
    quantity: Optional[int] = None
    
    model_config = {
        "from_attributes": True
    }

class RequestOut(RequestBase):
    id: int
    equipment_name: str
    quantity: Optional[int] = None
    status: str
    requested_by: int
    requested_by_name: str  
    status_changed_by: Optional[int] = None
    status_changed_by_name: Optional[str] = None  
    
    model_config = {
        "from_attributes": True
    }


#Validação Crime
class CrimeStatBase(BaseModel):
    villain: str
    crimes: str
    neighborhood: str
    date: date

class CrimeStat(CrimeStatBase):
    id: int

    model_config = {
        "from_attributes": True
    }


#Validação Alert
class AlertBase(BaseModel):
    location: str
    villain: str
    type: str

class AlertSchema(AlertBase):
    id: int

    model_config = {
        "from_attributes": True
    }


#Validação Token
class Token(BaseModel):
    access_token: str
    token_type: str