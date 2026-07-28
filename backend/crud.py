from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, aliased

from backend import schemas
from backend.models import Alert, CrimeStat, Request, RequestStatusEnum, Resource, User
from backend.security import hash_password, verify_password


def commit(db: Session) -> None:
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.scalar(select(User).where(User.username == username.strip()))


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def list_users(db: Session, limit: int = 100, offset: int = 0) -> list[User]:
    statement = select(User).order_by(User.name).limit(limit).offset(offset)
    return list(db.scalars(statement))


def create_user(db: Session, payload: schemas.UserCreate) -> User:
    user = User(
        name=payload.name,
        username=payload.username,
        hashed_password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    commit(db)
    db.refresh(user)
    return user


def update_user(db: Session, user: User, payload: schemas.UserUpdate) -> User:
    data = payload.model_dump(exclude_unset=True)
    password = data.pop("password", None)

    for field, value in data.items():
        setattr(user, field, value)

    if password:
        user.hashed_password = hash_password(password)

    commit(db)
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    commit(db)


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


def create_resource(db: Session, payload: schemas.ResourceCreate, user_id: int) -> Resource:
    resource = Resource(**payload.model_dump(), registered_by=user_id)
    db.add(resource)
    commit(db)
    db.refresh(resource)
    return resource


def get_resource(db: Session, resource_id: int) -> Resource | None:
    return db.get(Resource, resource_id)


def list_resources(db: Session, limit: int = 100, offset: int = 0) -> list[dict]:
    statement = (
        select(Resource, User.name.label("registered_by_name"))
        .join(User, Resource.registered_by == User.id)
        .order_by(Resource.name)
        .limit(limit)
        .offset(offset)
    )
    rows = db.execute(statement).all()
    return [
        {
            "id": resource.id,
            "name": resource.name,
            "type": resource.type,
            "quantity": resource.quantity,
            "status": resource.status,
            "registered_by": resource.registered_by,
            "registered_by_name": registered_by_name,
            "created_at": resource.created_at,
            "updated_at": resource.updated_at,
        }
        for resource, registered_by_name in rows
    ]


def update_resource(db: Session, resource: Resource, payload: schemas.ResourceUpdate) -> Resource:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    commit(db)
    db.refresh(resource)
    return resource


def delete_resource(db: Session, resource: Resource) -> None:
    db.delete(resource)
    commit(db)


def create_request(db: Session, payload: schemas.RequestCreate, user_id: int) -> Request:
    request = Request(**payload.model_dump(), requested_by=user_id)
    db.add(request)
    commit(db)
    db.refresh(request)
    return request


def get_request(db: Session, request_id: int) -> Request | None:
    return db.get(Request, request_id)


def list_requests(db: Session, user: User, limit: int = 100, offset: int = 0) -> list[dict]:
    creator = aliased(User)
    changer = aliased(User)
    statement = (
        select(
            Request,
            creator.name.label("requested_by_name"),
            changer.name.label("status_changed_by_name"),
        )
        .join(creator, Request.requested_by == creator.id)
        .outerjoin(changer, Request.status_changed_by == changer.id)
        .order_by(Request.id.desc())
        .limit(limit)
        .offset(offset)
    )
    if user.role.value == "Funcionário":
        statement = statement.where(Request.requested_by == user.id)

    rows = db.execute(statement).all()
    return [
        {
            "id": request.id,
            "equipment_name": request.equipment_name,
            "quantity": request.quantity,
            "status": request.status,
            "requested_by": request.requested_by,
            "requested_by_name": requested_by_name,
            "status_changed_by": request.status_changed_by,
            "status_changed_by_name": status_changed_by_name,
            "created_at": request.created_at,
            "updated_at": request.updated_at,
            "resolved_at": request.resolved_at,
        }
        for request, requested_by_name, status_changed_by_name in rows
    ]


def update_request_quantity(db: Session, request: Request, quantity: int) -> Request:
    request.quantity = quantity
    commit(db)
    db.refresh(request)
    return request


def update_request_status(
    db: Session,
    request: Request,
    status: RequestStatusEnum,
    changed_by: int,
) -> Request:
    request.status = status
    request.status_changed_by = changed_by
    request.resolved_at = datetime.now(timezone.utc)
    commit(db)
    db.refresh(request)
    return request


def get_crime_stats(db: Session) -> list[CrimeStat]:
    return list(db.scalars(select(CrimeStat).order_by(CrimeStat.date.desc())))


def get_alerts(db: Session) -> list[Alert]:
    return list(db.scalars(select(Alert).order_by(Alert.id.desc())))
