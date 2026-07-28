from __future__ import annotations

import enum
from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


def enum_values(enum_class: type[enum.Enum]) -> list[str]:
    return [str(member.value) for member in enum_class]


class RoleEnum(str, enum.Enum):
    ADMIN = "Admin"
    MANAGER = "Gerente"
    EMPLOYEE = "Funcionário"


class TypeEnum(str, enum.Enum):
    WEAPON = "Arma"
    ACCESSORY = "Acessório"
    VEHICLE = "Veículo"
    SUIT = "Traje"


class RequestStatusEnum(str, enum.Enum):
    PENDING = "Pendente"
    COMPLETED = "Concluído"
    REJECTED = "Recusado"


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, values_callable=enum_values),
        nullable=False,
        default=RoleEnum.EMPLOYEE,
    )

    registered_resources: Mapped[list[Resource]] = relationship(back_populates="registered_by_user")
    created_requests: Mapped[list[Request]] = relationship(
        back_populates="requested_by_user",
        foreign_keys="Request.requested_by",
    )
    changed_requests: Mapped[list[Request]] = relationship(
        back_populates="status_changed_by_user",
        foreign_keys="Request.status_changed_by",
    )


class Resource(TimestampMixin, Base):
    __tablename__ = "resources"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_resources_quantity_non_negative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    type: Mapped[TypeEnum] = mapped_column(
        Enum(TypeEnum, values_callable=enum_values),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    registered_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    registered_by_user: Mapped[User] = relationship(back_populates="registered_resources")

    @property
    def status(self) -> str:
        return "Disponível" if self.quantity > 0 else "Indisponível"


class Request(TimestampMixin, Base):
    __tablename__ = "requests"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_requests_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipment_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[RequestStatusEnum] = mapped_column(
        Enum(RequestStatusEnum, values_callable=enum_values),
        nullable=False,
        default=RequestStatusEnum.PENDING,
    )
    requested_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status_changed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    requested_by_user: Mapped[User] = relationship(
        back_populates="created_requests",
        foreign_keys=[requested_by],
    )
    status_changed_by_user: Mapped[User | None] = relationship(
        back_populates="changed_requests",
        foreign_keys=[status_changed_by],
    )


class CrimeStat(Base):
    __tablename__ = "crime_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    villain: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    crimes: Mapped[str] = mapped_column(String(100), nullable=False)
    neighborhood: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    villain: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
