from pydantic import BaseModel, Field
from backend.models import RoleEnum, TypeEnum
from datetime import date
from typing import Optional


#Validação User
class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    role: RoleEnum
    class Config:
        use_enum_values = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

#Validação Resource
class ResourceBase(BaseModel):
    name: str
    type: TypeEnum
    quantity: int
    status: Optional[str] = None
    class Config:
        use_enum_values = True

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int

    class Config:
        from_attributes = True

class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[TypeEnum] = None
    quantity: Optional[int] = None  
    status: Optional[str] = None

    class Config:
        use_enum_values = True

#Validação Request
class RequestBase(BaseModel):
    equipment_name: str
    status: Optional[str] = "Pendente"

class RequestCreate(RequestBase):
    quantity: Optional[int] = None 

class RequestUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[str] = 'Concluído'

class Request(RequestBase):
    id: int
    requested_by: int
    status_changed_by: Optional[int] = None
    quantity: Optional[int] = None

    class Config:
        from_attributes = True

#Validação Crime
class CrimeStatBase(BaseModel):
    villain: str
    crimes: str
    neighborhood: str
    date: date

class CrimeStat(CrimeStatBase):
    id: int

    class config:
        from_attributes = True

#Validação Alert
class AlertBase(BaseModel):
    location: str
    villain: str
    type: str

class Alert(AlertBase):
    id: int
    class Config:
        from_attributes = True


#Validação Token
class Token(BaseModel):
    access_token: str
    token_type: str