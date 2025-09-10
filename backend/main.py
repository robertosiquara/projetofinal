#🧠 Objetivo do Código
#Criar uma API com FastAPI para servir endpoints RESTful e arquivos estáticos 
#(como uma interface web em HTML/CSS/JS), organizada em módulos (roteadores),
#e conectada a um banco de dados via SQLAlchemy.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware 
import os
from backend.database import Base, engine
from backend.routers import users, resources, requests, dashboard, alerts, request_resource


#Instancia principal da aplicação
app = FastAPI(
    title="Central de Segurança - Indústrias Wayne",
    version="1.0.0",
    description="API para gerenciamento de segurança nas Indústrias Wayne"
)

# uso do mecanismo de segurança de navegador CORS para permitir o frontend acessar o fastapi em outro dominio.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)


#Verifica se exixte a pasta 'frontend'
if os.path.isdir("frontend"):
    app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
else:
    print("[AVISO] Diretório 'frontend' não encontrado. Arquivos estáticos não foram montados.")

app.include_router(users.router, prefix='/users', tags=['Usuários'])
app.include_router(resources.router, prefix='/resources', tags=['Recursos'])
app.include_router(dashboard.router, prefix= '/dashboard', tags= ['Dashboard'])
app.include_router(alerts.router, prefix='/alerts', tags=['Alertas'])
app.include_router(request_resource.router, prefix='/request_resources', tags=['Requisitar'])
app.include_router(requests.router, prefix='/requests', tags=['Requisições'])

#Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Rota principal
@app.get("/")
async def root():
    return RedirectResponse(url="/frontend/index.html")

@app.get("/index")
async def index():
    return RedirectResponse(url="/frontend/index.html")

@app.get("/index.html")
async def index_html():
    return RedirectResponse(url="/frontend/index.html")