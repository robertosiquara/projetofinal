from sqlalchemy import Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, validates, Mapped, mapped_column
import enum
from datetime import datetime
from typing import List
from backend.database import Base

class RoleEnum(str, enum.Enum):
    admin = 'Admin'
    gerente = 'Gerente'
    funcionario = 'Funcionário'

class TypeEnum(str, enum.Enum):
    arma = 'Arma'
    acessorio = "Acessório"
    veiculo = 'Veículo'
    traje = 'Traje'

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer,primary_key= True, index= True) 
    name: Mapped[str] = mapped_column(String(100), nullable= False, index= True)
    username: Mapped[str] = mapped_column(String(30), unique= True, nullable= False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable= False)
    registered: Mapped[List["Resource"]] = relationship(
        back_populates='register',
    )
    requests: Mapped[List["Request"]] = relationship(
        back_populates='user',
        foreign_keys="Request.requested_by"
    )
    requests_status: Mapped[List["Request"]] = relationship(
        back_populates='status_changer',
        foreign_keys="Request.status_changed_by"
    )

class Resource(Base):
    __tablename__ = 'resources'
    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    name: Mapped[str] = mapped_column(String(100), nullable= False, index= True)
    type: Mapped[TypeEnum] = mapped_column(Enum(TypeEnum), nullable= False)
    quantity: Mapped[int] = mapped_column(Integer, nullable= False)
    status: Mapped[str] = mapped_column(String(30), nullable= True)
    registered_by: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable= False)
    register: Mapped["User"] = relationship(
        back_populates='registered',
        foreign_keys=[registered_by]
    )

    @validates('quantity')
    def update_status_based_on_quantity(self, key, value):
        if value > 0:
            self.status = 'Disponível'
        else:
            self.status = 'Indisponível'
        return value
    
class Request(Base):
    __tablename__ = 'requests'
    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    equipment_name: Mapped[str] = mapped_column(String(100), nullable= False, index= True)
    quantity: Mapped[int] = mapped_column(Integer, nullable= True)
    status: Mapped[str] = mapped_column(String(20), default= 'Pendente', nullable= False)
    requested_by: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable= False)
    status_changed_by: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable= True)
    user: Mapped["User"] = relationship(
        back_populates='requests',
        foreign_keys=[requested_by]
    )
    status_changer: Mapped["User"] = relationship(
        back_populates='requests_status',
        foreign_keys=[status_changed_by]
    )

class CrimeStat(Base):
    __tablename__ = 'crime_stats'
    id: Mapped[int] = mapped_column(Integer, primary_key=  True, index= True)
    villain: Mapped[str] = mapped_column(String(100), nullable= False, index= True)
    crimes: Mapped[str] = mapped_column(String(100), nullable= False)
    neighborhood: Mapped[str] = mapped_column(String(100), nullable= False)
    date: Mapped[datetime] = mapped_column(DateTime, default= datetime.utcnow, nullable= False)

class Alert(Base):
    __tablename__ = 'alerts'
    id: Mapped[int] = mapped_column(Integer, primary_key= True, index= True)
    villain: Mapped[str] = mapped_column(String(100), nullable= False)
    location: Mapped[str] = mapped_column(String(100), nullable= False)
    type: Mapped[str] = mapped_column(String(100), nullable= False)