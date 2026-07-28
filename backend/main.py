from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.config import settings
from backend.database import Base, engine, get_db
from backend.routers import alerts, dashboard, requests, resources, users

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="3.0.0",
    description="API de gestão da Central de Segurança Wayne",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(resources.router, prefix="/resources", tags=["Recursos"])
app.include_router(requests.router, prefix="/requests", tags=["Solicitações"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alertas"])
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/frontend/index.html")


@app.get("/health", tags=["Sistema"])
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}
