# 🦇 Wayne Security Center

> Sistema completo de gerenciamento da Central de Segurança das Indústrias Wayne desenvolvido com **FastAPI**, **SQLAlchemy 2.0**, **MySQL**, **HTML5**, **CSS3** e **JavaScript ES6 Modules**.

O sistema simula a central de segurança da Wayne Enterprises, permitindo o gerenciamento de usuários, recursos, solicitações internas, estatísticas criminais, dashboard gerencial e monitoramento de alertas em tempo real.

---

# Demonstração

## Login

- Autenticação JWT
- Controle de acesso por perfis
- Login seguro

## Dashboard

- Indicadores em tempo real
- Recursos disponíveis
- Solicitações pendentes
- Estatísticas criminais
- Cards administrativos

## Recursos

Controle completo de:

- Veículos
- Trajes
- Armamentos
- Equipamentos
- Acessórios

## Solicitações

Funcionários podem solicitar recursos.

Gerentes e administradores podem:

- Aprovar
- Rejeitar
- Concluir

---

# Monitoramento de Alertas

Sistema inspirado na Central da Batcaverna.

Funcionalidades:

- Alerta visual em tela cheia
- Som de sirene
- Animação piscando
- Histórico automático
- Sequência contínua de ocorrências

Cada ocorrência permanece alguns segundos em destaque antes de entrar para o histórico.

---

# Tecnologias

## Backend

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0
- Pydantic V2
- Pydantic Settings
- JWT
- python-jose
- Passlib
- Bcrypt
- PyMySQL

## Banco de Dados

- MySQL 8

## Frontend

- HTML5
- CSS3
- JavaScript ES6 Modules

---

# Arquitetura

```
backend
│
├── auth.py
├── config.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
│
├── routers
│   ├── alerts.py
│   ├── dashboard.py
│   ├── requests.py
│   ├── resources.py
│   └── users.py
│
frontend
│
├── css
│   ├── settings
│   ├── generic
│   ├── objects
│   ├── elements
│   └── components
│
├── js
│   ├── components
│   ├── config
│   ├── pages
│   ├── services
│   └── utils
│
├── sounds
│
└── images
```

---

# Estrutura do Projeto

```
Wayne Security Center

Administrador
        │
        ▼

 Login JWT

        │

────────────── API FastAPI ──────────────

Usuários
Recursos
Solicitações
Dashboard
Alertas

──────────── SQLAlchemy ────────────────

MySQL

```

---

# Controle de Permissões

## Administrador

✔ Gerenciar usuários

✔ Gerenciar recursos

✔ Aprovar solicitações

✔ Dashboard

✔ Alertas

✔ Estatísticas

---

## Gerente

✔ Gerenciar recursos

✔ Aprovar solicitações

✔ Dashboard

✔ Alertas

❌ Gerenciar usuários

---

## Funcionário

✔ Visualizar recursos

✔ Solicitar recursos

✔ Consultar suas solicitações

❌ Dashboard Administrativo

❌ Aprovar solicitações

❌ Gerenciar usuários

---

# Banco de Dados

O projeto utiliza MySQL.

Principais tabelas:

- users
- resources
- requests
- alerts
- crime_stats

---

# Instalação

## Clone

```bash
git clone https://github.com/usuario/wayne-security.git
```

Entre na pasta

```bash
cd wayne-security
```

---

## Ambiente Virtual

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Instale as dependências

```bash
pip install -r requirements.txt
```

---

# Configure o .env

Exemplo:

```env
DATABASE_URL=mysql+pymysql://root:senha@localhost/wayne_security

SECRET_KEY=sua_chave_super_secreta_com_mais_de_32_caracteres

ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

---

# Banco

Criar

```sql
CREATE DATABASE wayne_security;
```

Executar

```
database.sql
```

---

# Executando

```bash
python -m uvicorn backend.main:app --reload
```

Abrir

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

Health Check

```
http://localhost:8000/health
```

---

# Usuários de Demonstração

Administrador

```
Usuário

batman

Senha

darkknight
```

Gerente

```
Usuário

alfred

Senha

wayne
```

Funcionário

```
Usuário

employee1

Senha

wayne
```

---

# Segurança

- JWT Bearer Token

- Senhas criptografadas com BCrypt

- Controle de permissões por Roles

- Rotas protegidas

- Validação completa com Pydantic

---

# Funcionalidades

## Usuários

- Login
- Cadastro
- Atualização
- Exclusão

---

## Recursos

- Cadastro

- Atualização

- Estoque

- Disponibilidade

---

## Solicitações

- Criar

- Aprovar

- Rejeitar

- Concluir

- Histórico

---

## Dashboard

- Recursos disponíveis

- Solicitações

- Indicadores

- Estatísticas

---

## Alertas

- Ocorrências em tempo real

- Tela cheia

- Sirene

- Histórico

---

# Melhorias Implementadas

✔ Arquitetura modular

✔ SQLAlchemy 2.0

✔ Pydantic V2

✔ ES6 Modules

✔ CSS organizado

✔ Separação por responsabilidades

✔ Dashboard atualizado

✔ Sistema de Alertas em Tempo Real

✔ Componentização do Frontend

✔ Autenticação JWT

✔ Controle de Permissões

---

# Melhorias Futuras

- WebSocket para alertas em tempo real

- Integração com câmeras IP

- Upload de imagens

- Reconhecimento Facial

- Geolocalização

- IA para detecção automática

- Notificações Push

- Docker

- CI/CD

- Testes Automatizados

- Alembic

---

# Licença

Projeto desenvolvido exclusivamente para fins educacionais e demonstração de arquitetura de software.

---

# Autor

**Roberto Siquara**

Transição de carreira para Desenvolvimento de Software.

Projeto desenvolvido para estudos de:

- FastAPI

- SQLAlchemy 2.0

- Arquitetura Backend

- JavaScript Moderno

- CSS

- APIs REST

- JWT

- MySQL

- Engenharia de Software