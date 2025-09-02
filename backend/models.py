from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import validates, relationship
from backend.database import Base
from datetime import datetime
import enum

#Valores definidos para tipos de usuario. 
class RoleEnum(str, enum.Enum):
    admin = "Admin"
    gerente = "Gerente"
    funcionario = "Funcionário"

#Valores definidos para tipos de equipamentos. 
class TypeEnum(str, enum.Enum):
    veiculo = "Veiculo"
    acessorio = "Acessório"
    arma = "Arma"
    traje = 'Traje'
    
  
#Classes de Objetos para criação das tabelas do banco de dados.
class User(Base):
    __tablename__= 'users'
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String(100), nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    requests = relationship(
        "Request",
        back_populates="user",
        foreign_keys="Request.requested_by"
    )
    changed_requests = relationship(
        "Request",
        back_populates="status_changer",
        foreign_keys="Request.status_changed_by"
    )

class Resource(Base):
    __tablename__= 'resources'
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(TypeEnum), nullable=False)
    quantity= Column(Integer, nullable=False)
    status = Column(String(20), nullable=True)

    @validates('quantity')
    def update_status_based_on_quantity(self, key, value):
        # Atualiza o status com base na nova quantidade
        if value > 0:
            self.status = "Disponível"
        else:
            self.status = "Indisponível"
        return value

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    equipment_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=True)
    status = Column(String(20), default="Pendente", nullable=False)
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    status_changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    user = relationship(
        "User",
        back_populates="requests",
        foreign_keys=[requested_by]
    )
    status_changer = relationship(
        "User",
        back_populates="changed_requests",
        foreign_keys=[status_changed_by]
    )
class CrimeStat(Base):
    __tablename__ = "crime_stats"
    id = Column(Integer, primary_key=True, index=True)
    villain = Column(String(100), nullable=False)
    crimes = Column(Integer, nullable=False)
    neighborhood = Column(String(100))
    date = Column(DateTime, default=datetime.utcnow, nullable=False)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255))  # Specify length
    villain = Column(String(255))   # Specify length
    type = Column(String(255))