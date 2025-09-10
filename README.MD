# Central de Segurança Indústrias Wayne

O **Central de Segurança Indústrias Wayne** é um sistema web desenvolvido para gerenciar operações de segurança das Indústrias Wayne.  

Ele oferece:  
- Autenticação de usuários com diferentes níveis de acesso (`admin`, `gerente`, `funcionário`).  
- Gerenciamento de recursos (veículos, armas, acessórios, trajes).  
- Solicitação e aprovação de novos equipamentos.  
- Exibição de alertas de segurança com efeitos visuais e sonoros.  
- Visualização de estatísticas de crimes, recursos e atividades dos usuários em um dashboard interativo.  
- Operações CRUD (criar, ler, atualizar, deletar) para recursos e solicitações.  
- Página de boas-vindas exibindo o nome do usuário logado (e.g., *“Bem-vindo, Bruce Wayne!”*).  

---

## 🚀 Funcionalidades
- **Autenticação**: Login com JWT (JSON Web Tokens).  
- **Boas-Vindas**: Mensagem personalizada no `welcome.html`.  
- **Gerenciamento de Recursos**: CRUD com status automático (Disponível/Indisponível).  
- **Solicitações de Recursos**: gerentes/admins solicitam;  funcionários concluem.  
- **Dashboard**: Gráficos de crimes por vilão e bairro, recursos por tipo e disponibilidade e atividades dos usuários.  
- **Alertas**: Tela piscante e som de sirene para alertas de segurança.  
- **Controle de Acesso**: Funcionalidades restritas por papel.  
- **Logout**: Finaliza sessão e redireciona para o login.  

---

## 🛠 Tecnologias Utilizadas
**Backend**  
- Python 3.8+  
- FastAPI  
- SQLAlchemy  
- MySQL (gerenciado pelo MySQL Workbench)
- python-jose (JWT)  
- passlib (hash de senhas com bcrypt) 
- PyMySQL (driver para conectar Python ao MySQL) 

**Frontend**  
- HTML5, CSS3, JavaScript (ES6)  
- Chart.js  

**Outros**  
- Uvicorn (servidor ASGI)  
- Markdown (documentação)  

---

## 📦 Pré-requisitos
- Python 3.8+  
- pip (gerenciador de pacotes)  
- Navegador web moderno (Chrome, Firefox, etc.)  
- (Opcional) Git  
- (Opcional) VS Code ou outro editor  

---

## ⚙️ Instalação
1. **Clone o Repositório**  
   ```bash
   git clone https://github.com/seu-usuario/central-seguranca-wayne.git
   cd central-seguranca-wayne
   ```

2. **Crie e Ative o Ambiente Virtual**  
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as Dependências**  
   ```bash
   pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart pymysql
   ```

4. **Configure o Banco de Dados**  
   - Crie o bando de dados no MySQLWorkbench, conforme arquivo database.sql
   - Ao inicializar a aplicação cria as tabelas: 
   - Insira os dados das tabelas no MySQLWorkbench, conforme arquivo database.sql 
  
5. **Estrutura de Diretórios**  
   ```
   central-seguranca-wayne/
   ├── backend/
   │   ├── main.py            # Ponto de entrada FastAPI
   │   ├── models.py          # Modelos do banco
   │   ├── schemas.py         # Schemas Pydantic
   │   ├── crud.py            # Funções CRUD
   │   ├── auth.py            # Autenticação JWT
   │   ├── database.py        # Configuração banco
   │   ├── routers/           # Endpoints
   │       ├── users.py
   │       ├── resources.py
   │       ├── requests.py
   │       ├── request_resource.py
   │       ├── dashboard.py
   │       └── alerts.py   
   ├── frontend/
   │   ├── css/style.css
   │   ├── js/script.js
   │   ├── sounds/siren.mp3
   │   ├── index.html
   │   ├── welcome.html
   │   ├── dashboard.html
   │   ├── users.html
   │   ├── resources.html
   │   ├── request_resource.html
   │   ├── requests.html
   │   ├── alerts.html
   │   ├── Wayne.webp
   │   └── icone.png
   ├── venv/
   ├── requiriments.txt     # Lista todas as dependencias 
   ├── lista.py             # Cria dados para tabela de crimes
   ├── database.sql         # Dados para criação do banco de dados e inclusao dedados nas tabelas
   ├── senha.py             # Criar hash de senhas
   └── README.md
   ```

---

## ▶️ Execução
### Backend
```bash
uvicorn backend.main:app --reload
```
Disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)  

### Frontend
- Acesse diretamente: [http://localhost:8000/frontend/index.html](http://localhost:8000/frontend/index.html)  
- Ou rode servidor estático:
  ```bash
  cd frontend
  python -m http.server 8000
  ```

---

## 🔑 Credenciais Padrão
- Usuário: `batman`  
- Senha: `darkknight`  
- Papel: `admin`  
- Nome: `Bruce`  

---

## 📖 Uso
- **Login**: `index.html`  
- **Página de Boas-Vindas**: `welcome.html` → *“Bem-vindo, <nome>!”*  
- **Admin**: Acesso a todas as funcionalidades.  
- **Gerente**: Gerenciamento de usuários gerenciamento de recursos e solicitações.  
- **Funcionário**: Conclusão de solicitações boas-vindas.  

---

## 📡 Endpoints da API
Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

**Exemplo – Login**  
```http
POST /users/token
username=batman&password=darkknight
```

**Recursos**  
- `GET /resources/` → lista recursos  
- `POST /resources/` → cria recurso  
- `PUT /resources/{id}` → edita recurso 
- `DELETE /resources/{id}` → deleta recurso 

**Solicitações**  
- `GET /requests/` → lista status 
- `POST /request_resources/` → cria solicitação  
- `PUT /requests/{id}` → atualiza status 


**Dashboard**  
- `GET /dashboard/stats` → estatísticas de crimes
- `GET /dashboard/resources` → estatísticas  de recursos
- `GET /dashboard/requests` → estatísticas  de requisições

**Alertas**  
- `GET /alerts/` → lista alertas  

---

## 🐞 Resolução de Problemas
- **Erro 404 em /resources/** → verifique inclusão em `main.py`.  
- **Erro 422** → confirme body enviado corresponde ao schema.  
- **Nome não exibido no welcome** → inclua `name` no payload do JWT.  
- **Dashboard sem gráficos** → confirme inclusão do Chart.js.  

---

## 🧪 Testes
### Backend
```bash
uvicorn backend.main:app --reload
curl -X POST "http://localhost:8000/users/token" -d "username=batman&password=darkknight" -H "Content-Type: application/x-www-form-urlencoded"
```

### Frontend
- Login via `index.html`  
- Testar CRUD de recursos e solicitações  
- Conferir dashboard e alertas  


---

## 🤝 Contribuição
1. Fork o repositório  
2. Crie uma branch:  
   ```bash
   git checkout -b minha-feature
   ```
3. Commit:  
   ```bash
   git commit -m "Adiciona minha feature"
   ```
4. Push:  
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request  

---

## 📦 Empacotamento
```bash
zip -r central_seguranca_wayne.zip .
```

---


## 📬 Contato
Para dúvidas ou sugestões:  
- Equipe fictícia da Wayne Enterprises  
- Desenvolvedor principal: *Roberto Siquara*  

---

## 🙏 Agradecimentos
- Equipe fictícia das Indústrias Wayne  
- Bibliotecas open-source: **FastAPI, SQLAlchemy**  