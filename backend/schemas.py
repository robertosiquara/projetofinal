from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.models import RequestStatusEnum, RoleEnum, TypeEnum


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class TextValidationMixin:
    @field_validator("name", "username", "equipment_name", mode="before", check_fields=False)
    @classmethod
    def normalize_text(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
        if value == "":
            raise ValueError("O campo não pode ficar vazio.")
        return value


class UserBase(TextValidationMixin, ORMModel):
    name: str = Field(min_length=3, max_length=100)
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    role: RoleEnum


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserUpdate(TextValidationMixin, ORMModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    username: str | None = Field(default=None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str | None = Field(default=None, min_length=8, max_length=72)
    role: RoleEnum | None = None


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ResourceBase(TextValidationMixin, ORMModel):
    name: str = Field(min_length=2, max_length=100)
    type: TypeEnum
    quantity: int = Field(ge=0, le=1_000_000)


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(TextValidationMixin, ORMModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    type: TypeEnum | None = None
    quantity: int | None = Field(default=None, ge=0, le=1_000_000)


class ResourceOut(ResourceBase):
    id: int
    status: str
    registered_by: int
    registered_by_name: str | None = None
    created_at: datetime
    updated_at: datetime


class RequestCreate(TextValidationMixin, ORMModel):
    equipment_name: str = Field(min_length=2, max_length=100)
    quantity: int = Field(default=1, ge=1, le=100_000)


class RequestQuantityUpdate(ORMModel):
    quantity: int = Field(ge=1, le=100_000)


class RequestStatusUpdate(ORMModel):
    status: RequestStatusEnum

    @field_validator("status")
    @classmethod
    def reject_pending_status(cls, value: RequestStatusEnum) -> RequestStatusEnum:
        if value == RequestStatusEnum.PENDING:
            raise ValueError("Use apenas Concluído ou Recusado.")
        return value


class RequestOut(ORMModel):
    id: int
    equipment_name: str
    quantity: int
    status: RequestStatusEnum
    requested_by: int
    requested_by_name: str | None = None
    status_changed_by: int | None = None
    status_changed_by_name: str | None = None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None


class CrimeStatOut(ORMModel):
    id: int
    villain: str
    crimes: str
    neighborhood: str
    date: datetime


class AlertOut(ORMModel):
    id: int
    location: str
    villain: str
    type: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
