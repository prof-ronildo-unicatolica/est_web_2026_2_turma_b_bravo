# Backlog de Tasks e Detalhamento de Sprints

**Projeto:** Sistema de Gestão Hoteleira — Estágio II (2026.2)  
**Equipe:** Bravo (Turma B)  

---

## 📌 Guia de Git & Versionamento para Estagiários

Para cada subtarefa abaixo, o estagiário responsável deve seguir rigorosamente os passos de versionamento:

1. **Atualizar a branch base:**
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. **Criar a branch da subtarefa:**
   ```bash
   git checkout -b <nome-da-branch-indicado-na-subtask>
   ```
3. **Desenvolver o código e testar localmente.**
4. **Adicionar alterações e fazer commit padronizado (Conventional Commits):**
   ```bash
   git add .
   git commit -m "<mensagem-de-commit-indicada-na-subtask>"
   ```
5. **Enviar a branch para o GitHub:**
   ```bash
   git push origin <nome-da-branch-indicado-na-subtask>
   ```
6. **Abrir Pull Request (PR):**
   - **Base/Destino:** `develop`
   - **Título:** `[Sprint X] Feat/Fix/Chore/Test: Descrição resumida`
   - Preencher a descrição com o que foi feito, como testar e marcar o checklist de aceite.

---

## 🚀 Sprint 1 — Fundação e Setup (Aula 02)

> **Objetivo:** Garantir a execução lisa da stack local (Docker), validar contratos de API e alinhar a estrutura de pastas.

### Tarefas do Backend (Core Service)

#### 📋 **TSK-101: Executar e validar migrações SQL iniciais no PostgreSQL (`alembic upgrade head`)**

* - [ ] **SUB-101.1: Validação do Ambiente Local e Docker Postgres**
  * **Descrição:** Garantir que o container do banco PostgreSQL esteja ativo e com as credenciais corretas configuradas no arquivo `.env`.
  * **Como realizar:**
    1. Copie o arquivo `.env.example` para `.env` na raiz do projeto (se ainda não existir).
    2. Verifique as credenciais em `.env` (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DATABASE_URL`).
    3. Execute o comando no terminal: `docker compose up -d postgres`.
    4. Confirme que o container subiu sem erros com `docker compose ps`.
  * **Branch:** `feature/db-docker-setup`
  * **Commit:** `chore(docker): valida configuracao local do postgresql`

* - [ ] **SUB-101.2: Execução das Migrações Iniciais via Alembic**
  * **Descrição:** Executar o utilitário do Alembic para aplicar todas as migrações SQL pendentes na base de dados.
  * **Como realizar:**
    1. Com o container do Postgres rodando, execute no terminal: `alembic upgrade head`.
    2. Verifique nos logs se as migrações foram aplicadas com sucesso até a versão `head`.
    3. (Opcional) Conecte no banco via DBeaver ou cliente SQL e confirme a criação das tabelas base e da tabela `alembic_version`.
  * **Branch:** `feature/db-alembic-migrations`
  * **Commit:** `feat(db): executa e valida migracoes iniciais do alembic`

---

#### 📋 **TSK-102: Mapear os modelos iniciais do domínio no SQLAlchemy**

* - [ ] **SUB-102.1: Mapear Modelo `Cidade`**
  * **Descrição:** Criar a classe de modelo ORM do SQLAlchemy para a entidade `Cidade`.
  * **Como realizar:**
    1. Crie ou edite o arquivo `app/models/cidade.py`.
    2. Herde da classe `Base` do SQLAlchemy e defina as colunas: `id` (Integer, PK), `nome` (String(100), nullable=False) e `estado` (String(2), nullable=False).
    3. Adicione a representação `__repr__` para facilitar depuração.
  * **Branch:** `feature/model-cidade`
  * **Commit:** `feat(models): implementa modelo sqlalchemy da entidade Cidade`

* - [ ] **SUB-102.2: Mapear Modelo `Hotel`**
  * **Descrição:** Criar a classe de modelo ORM para a entidade `Hotel` com chave estrangeira apontando para `Cidade`.
  * **Como realizar:**
    1. Crie ou edite o arquivo `app/models/hotel.py`.
    2. Defina as colunas: `id` (Integer, PK), `nome` (String(150)), `cidade_id` (Integer, ForeignKey('cidades.id')), `estrelas` (Integer) e `diaria` (Float).
    3. Crie o relacionamento SQLAlchemy `cidade = relationship("Cidade", back_populates="hoteis")`.
  * **Branch:** `feature/model-hotel`
  * **Commit:** `feat(models): implementa modelo sqlalchemy da entidade Hotel com FK`

* - [ ] **SUB-102.3: Mapear Modelo `Usuario` Inicial**
  * **Descrição:** Estruturar o modelo da tabela de usuários antes da implementação completa da autenticação JWT.
  * **Como realizar:**
    1. Crie ou edite o arquivo `app/models/usuario.py`.
    2. Defina as colunas: `id` (Integer, PK), `nome` (String(100)), `email` (String(150), unique=True, index=True), `senha_hash` (String(255)) e `is_admin` (Boolean, default=False).
  * **Branch:** `feature/model-usuario`
  * **Commit:** `feat(models): cria estrutura inicial do modelo Usuario`

* - [ ] **SUB-102.4: Centralizar Registro dos Modelos no Alembic**
  * **Descrição:** Garantir que todos os modelos criados sejam importados centralizadamente para que o Alembic consiga identificar alterações de esquema.
  * **Como realizar:**
    1. Edite o arquivo `app/models/__init__.py` (ou `alembic/env.py`).
    2. Importe `Base`, `Cidade`, `Hotel` e `Usuario`.
    3. Garanta que no `alembic/env.py` a variável `target_metadata = Base.metadata` esteja apontando corretamente.
  * **Branch:** `chore/alembic-models-import`
  * **Commit:** `chore(db): registra modelos no metadata do alembic`

---

#### 📋 **TSK-103: Verificar o health check dos serviços em `GET /api/v1/health`**

* - [ ] **SUB-103.1: Implementar Endpoint HTTP de Health Check**
  * **Descrição:** Criar uma rota leve de diagnóstico que valida o funcionamento da API e a conectividade com o banco de dados.
  * **Como realizar:**
    1. Abra `app/api/v1/health.py` (ou equivalente na pasta de endpoints).
    2. Crie a rota `@router.get("/health")` injetando a sessão do banco `db: Session = Depends(get_db)`.
    3. Execute uma query simples de teste (ex: `db.execute(text("SELECT 1"))`).
    4. Retorne o payload JSON: `{"status": "ok", "database": "online"}` com status code HTTP 200.
  * **Branch:** `feature/api-health-check`
  * **Commit:** `feat(api): implementa endpoint de health check com teste no banco`

* - [ ] **SUB-103.2: Adicionar Teste Automatizado para o Health Check**
  * **Descrição:** Escrever teste unitário/integração usando Pytest para garantir que a rota de health check responda 200 OK.
  * **Como realizar:**
    1. Crie o arquivo `tests/test_health.py`.
    2. Escreva a função de teste `def test_health_check(client):`.
    3. Faça a requisição `response = client.get("/api/v1/health")`.
    4. Adicione as asserções: `assert response.status_code == 200` e `assert response.json()["status"] == "ok"`.
    5. Rode `pytest` no terminal para verificar a aprovação do teste.
  * **Branch:** `test/api-health-check`
  * **Commit:** `test(health): adiciona teste unitario para endpoint de status`

---

### Tarefas do Frontend

#### 📋 **TSK-104: Limpar telas de demonstração acadêmica e montar o Shell de Layout**

* - [ ] **SUB-104.1: Limpeza do Template Inicial React/Vite**
  * **Descrição:** Remover códigos de exemplo, contadores e estilos padrões não utilizados do template Vite.
  * **Como realizar:**
    1. Remova arquivos e imagens de exemplo não utilizadas na pasta `frontend/src/` (ex: `App.css`, logos SVG).
    2. Limpe a estrutura do `App.jsx` mantendo apenas a estrutura base limpa.
    3. Rode `npm run dev` e verifique se a página carrega sem erros no console F12.
  * **Branch:** `chore/frontend-cleanup`
  * **Commit:** `chore(frontend): remove templates de demonstracao do vite`

* - [ ] **SUB-104.2: Construir Componentes `Navbar` e `Footer`**
  * **Descrição:** Criar os componentes reutilizáveis de barra de navegação superior e rodapé institucional.
  * **Como realizar:**
    1. Crie `src/components/Navbar.jsx` com a logo do hotel, links de navegação ("Início", "Hotéis", "Entrar") e estilização Bootstrap/CSS.
    2. Crie `src/components/Footer.jsx` com informações de direitos autorais e links úteis.
    3. Exporte ambos os componentes.
  * **Branch:** `feature/frontend-navbar-footer`
  * **Commit:** `feat(frontend): cria componentes de Navbar e Footer`

* - [ ] **SUB-104.3: Montar o Shell de Layout Principal**
  * **Descrição:** Criar o componente de Layout que envolve as páginas com o Navbar no topo e Footer no rodapé.
  * **Como realizar:**
    1. Crie `src/components/Layout.jsx`.
    2. Renderize `<Navbar />`, `<main className="container my-4">{children}</main>` e `<Footer />`.
    3. Atualize o `App.jsx` para estruturar a renderização dentro do `<Layout>`.
  * **Branch:** `feature/frontend-layout-shell`
  * **Commit:** `feat(frontend): integra Shell de Layout com Navbar e Footer no App`

---

#### 📋 **TSK-105: Configurar cliente de requisições conectando na URL `http://localhost:8000`**

* - [ ] **SUB-105.1: Configurar Cliente HTTP Axios com `.env`**
  * **Descrição:** Instalar e configurar a instância centralizada do Axios utilizando variável de ambiente.
  * **Como realizar:**
    1. Execute `npm install axios` no diretório do frontend.
    2. Crie/Edite o arquivo `.env` no frontend definindo `VITE_API_URL=http://localhost:8000/api/v1`.
    3. Crie `src/services/api.js` importando Axios e criando a instância: `const api = axios.create({ baseURL: import.meta.env.VITE_API_URL })`.
    4. Exporte a instância `api` por padrão.
  * **Branch:** `feature/frontend-api-client`
  * **Commit:** `feat(frontend): configura cliente axios parametrizado por env`

* - [ ] **SUB-105.2: Testar Conexão HTTP com o Health Check da API**
  * **Descrição:** Validar se o frontend consegue se comunicar com o backend local sem erros de CORS.
  * **Como realizar:**
    1. No `App.jsx` ou em um componente de teste, adicione um `useEffect` realizando chamada `api.get('/health')`.
    2. Exiba o resultado da chamada no console ou na tela.
    3. Caso ocorra erro de CORS, certifique-se de que o `CORSMiddleware` esteja configurado no FastAPI backend.
  * **Branch:** `feature/frontend-health-integration`
  * **Commit:** `feat(frontend): valida chamada HTTP para o health check do backend`

---

### Critérios de Aceite (DoD - Sprint 1)
1. ✅ `docker compose up` sobe sem erros na máquina de qualquer integrante.
2. ✅ Todos os integrantes realizaram checkout na branch `develop` e abriram pelo menos 1 Pull Request aprovado.

---

## 🔑 Sprint 2 — Autenticação & Autorização JWT + RBAC (Aula 03) ⭐

> **Objetivo:** Substituir a autenticação mock por hash bcrypt seguro, geração de JWT e controle de papéis (Cliente vs Admin).

### Tarefas do Backend

#### 📋 **TSK-201: Model & Migration de Usuário com Seed Admin**

* - [ ] **SUB-201.1: Refinar o Modelo `Usuario` com Restrições**
  * **Descrição:** Garantir que o modelo em `app/models/usuario.py` contenha todas as restrições necessárias para o módulo de Auth.
  * **Como realizar:**
    1. Em `app/models/usuario.py`, verifique as colunas: `id`, `nome`, `email` (único, indexado), `senha_hash`, `is_admin` (Boolean, default=False), `created_at` (DateTime).
    2. Adicione validações ou índices adicionais se necessário.
  * **Branch:** `feature/auth-user-model`
  * **Commit:** `feat(models): refina modelo Usuario com campos temporais e restricoes`

* - [ ] **SUB-201.2: Gerar e Aplicar Migração Alembic para `usuarios`**
  * **Descrição:** Criar o script de migração contendo a tabela de usuários e executá-lo no PostgreSQL.
  * **Como realizar:**
    1. Execute no terminal: `alembic revision --autogenerate -m "create usuarios table"`.
    2. Inspecione o arquivo criado em `alembic/versions/` para validar a tabela `usuarios`.
    3. Execute `alembic upgrade head` para aplicar no banco de dados.
  * **Branch:** `feature/auth-user-migration`
  * **Commit:** `feat(db): gera e aplica migracao alembic para tabela de usuarios`

* - [ ] **SUB-201.3: Criar Script de Seed para Usuário Admin Padrão**
  * **Descrição:** Inserir automaticamente um usuário administrador inicial no banco de dados.
  * **Como realizar:**
    1. Crie um script `app/db/seed.py` (ou insira diretamente na migração Alembic).
    2. Criptografe a senha "admin123" usando bcrypt.
    3. Insira o registro com e-mail `admin@hotel.com` e `is_admin=True`.
  * **Branch:** `feature/auth-admin-seed`
  * **Commit:** `feat(db): adiciona script de seed para usuario admin padrao`

---

#### 📋 **TSK-202: Módulo de Segurança Backend**

* - [ ] **SUB-202.1: Utilitários de Hash de Senha em `app/core/security.py`**
  * **Descrição:** Implementar as funções de hashing e verificação de senhas com `passlib` / `bcrypt`.
  * **Como realizar:**
    1. Instale `passlib[bcrypt]` (se necessário).
    2. Em `app/core/security.py`, instancie `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`.
    3. Crie a função `get_password_hash(password: str) -> str`.
    4. Crie a função `verify_password(plain_password: str, hashed_password: str) -> bool`.
  * **Branch:** `feature/auth-security-password-hash`
  * **Commit:** `feat(security): cria utilitarios de hash e verificacao de senha bcrypt`

* - [ ] **SUB-202.2: Utilitários de Token JWT em `app/core/security.py`**
  * **Descrição:** Implementar a geração e decodificação de tokens JWT com expiração parametrizada.
  * **Como realizar:**
    1. Em `app/core/security.py`, importe `jwt` e as configurações em `app/core/config.py` (`SECRET_KEY`, `ALGORITHM`).
    2. Crie a função `create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str`.
    3. Adicione o tempo de expiração padrão (ex: 30 minutos) na claim `exp`.
  * **Branch:** `feature/auth-security-jwt`
  * **Commit:** `feat(security): implementa geracao de tokens JWT com expiracao`

---

#### 📋 **TSK-203: Serviço & Schemas de Autenticação**

* - [ ] **SUB-203.1: Criar Schemas Pydantic em `app/schemas/auth.py`**
  * **Descrição:** Definir as estruturas de validação de dados para registro, login e resposta de token.
  * **Como realizar:**
    1. Crie o arquivo `app/schemas/auth.py`.
    2. Crie a classe `UserCreate` (email: EmailStr, password: str, nome: str).
    3. Crie a classe `UserLogin` (email: EmailStr, password: str).
    4. Crie a classe `Token` (access_token: str, token_type: str = "bearer").
    5. Crie a classe `UserResponse` (id: int, nome: str, email: str, is_admin: bool).
  * **Branch:** `feature/auth-schemas`
  * **Commit:** `feat(schemas): cria contratos pydantic para operacoes de autenticacao`

* - [ ] **SUB-203.2: Implementar Lógica de Negócio em `app/services/auth_service.py`**
  * **Descrição:** Desenvolver as regras de cadastro de novos usuários e validação de login.
  * **Como realizar:**
    1. Crie `app/services/auth_service.py`.
    2. Método `register_user(db, user_in)`: verifica se e-mail já existe (retorna erro HTTP 409 se existir), gera o hash da senha e salva no banco.
    3. Método `authenticate_user(db, email, password)`: busca usuário pelo e-mail, valida a senha com `verify_password` e retorna o modelo do usuário ou `None`.
  * **Branch:** `feature/auth-service-logic`
  * **Commit:** `feat(services): implementa regras de negocio de registro e login em auth_service`

---

#### 📋 **TSK-204: Guards e Dependências FastAPI (RBAC)**

* - [ ] **SUB-204.1: Implementar Dependência `get_current_user` em `app/api/deps.py`**
  * **Descrição:** Extrair o token Bearer do cabeçalho da requisição e carregar o usuário autenticado.
  * **Como realizar:**
    1. Em `app/api/deps.py`, configure `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")`.
    2. Crie a função `async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme))`.
    3. Decodifique o JWT, extraia o `sub` (e-mail/id), consulte no banco e lance `HTTPException(401)` caso inválido.
  * **Branch:** `feature/auth-deps-current-user`
  * **Commit:** `feat(deps): cria dependencia get_current_user para injetar usuario autenticado`

* - [ ] **SUB-204.2: Implementar Dependência `get_current_admin` com Checagem RBAC**
  * **Descrição:** Proteger rotas restritas garantindo que o usuário possua papel de administrador.
  * **Como realizar:**
    1. Em `app/api/deps.py`, crie `def get_current_admin(current_user: Usuario = Depends(get_current_user))`.
    2. Verifique se `not current_user.is_admin`. Se for verdadeiro, lance `HTTPException(status_code=403, detail="Acesso negado: Requer privilégios de administrador")`.
    3. Retorne `current_user`.
  * **Branch:** `feature/auth-deps-admin`
  * **Commit:** `feat(deps): cria guarda get_current_admin com verificacao RBAC (403)`

---

#### 📋 **TSK-205: Endpoints HTTP de Autenticação**

* - [ ] **SUB-205.1: Implementar Endpoint `POST /api/v1/auth/register`**
  * **Descrição:** Rota pública para autocadastro de novos clientes.
  * **Como realizar:**
    1. Em `app/api/v1/auth.py`, crie a rota `@router.post("/register", response_model=UserResponse, status_code=201)`.
    2. Injete `user_in: UserCreate` e `db: Session = Depends(get_db)`.
    3. Invoque `auth_service.register_user` e retorne o usuário cadastrado.
  * **Branch:** `feature/auth-endpoint-register`
  * **Commit:** `feat(api): implementa endpoint de cadastro de clientes /auth/register`

* - [ ] **SUB-205.2: Implementar Endpoint `POST /api/v1/auth/login`**
  * **Descrição:** Rota pública para autenticação de credenciais e emissão do Token JWT.
  * **Como realizar:**
    1. Em `app/api/v1/auth.py`, crie a rota `@router.post("/login", response_model=Token)`.
    2. Autentique o usuário usando `auth_service.authenticate_user`.
    3. Gere o token JWT usando `create_access_token` e retorne `{"access_token": token, "token_type": "bearer"}`.
  * **Branch:** `feature/auth-endpoint-login`
  * **Commit:** `feat(api): implementa endpoint de login com retorno de JWT`

* - [ ] **SUB-205.3: Implementar Endpoint `GET /api/v1/auth/me`**
  * **Descrição:** Rota protegida para obtenção dos dados do usuário logado.
  * **Como realizar:**
    1. Em `app/api/v1/auth.py`, crie a rota `@router.get("/me", response_model=UserResponse)`.
    2. Injete `current_user: Usuario = Depends(get_current_user)`.
    3. Retorne `current_user`.
  * **Branch:** `feature/auth-endpoint-me`
  * **Commit:** `feat(api): implementa endpoint de consulta do perfil logado /auth/me`

---

#### 📋 **TSK-206: Suíte de Testes de Integração com Pytest**

* - [ ] **SUB-206.1: Configurar Fixtures de Banco e Cliente em `tests/conftest.py`**
  * **Descrição:** Preparar a infraestrutura de testes isolando o banco de dados.
  * **Como realizar:**
    1. Em `tests/conftest.py`, configure a fixture `db_session` para limpar as tabelas antes de cada teste.
    2. Configure a fixture `client` (usando `TestClient` do FastAPI) sobrescrevendo a dependência `get_db`.
  * **Branch:** `test/auth-fixtures`
  * **Commit:** `test(auth): configura fixtures de banco e cliente HTTP no conftest`

* - [ ] **SUB-206.2: Testar Fluxos Principais de Cadastro e Login em `tests/test_auth.py`**
  * **Descrição:** Garantir cobertura automatizada para os cenários de sucesso e erro no Auth.
  * **Como realizar:**
    1. Crie `tests/test_auth.py`.
    2. `test_register_user_success`: verifica cadastro válido (201).
    3. `test_register_duplicate_email`: verifica tentativa de reuso de e-mail (409).
    4. `test_login_success`: verifica login correto gerando token (200).
    5. `test_login_wrong_password`: verifica senha incorreta (401).
    6. Execute `pytest tests/test_auth.py` e garanta aprovação de 100%.
  * **Branch:** `test/auth-service-endpoints`
  * **Commit:** `test(auth): implementa testes de cadastro, login e tratamento de erros`

* - [ ] **SUB-206.3: Testar Controle de Acesso Admin (RBAC)**
  * **Descrição:** Validar que clientes normais recebem HTTP 403 ao tentar acessar recursos restritos de administrador.
  * **Como realizar:**
    1. Em `tests/test_auth.py`, crie teste tentando acessar rota de admin com token de cliente comum -> `assert response.status_code == 403`.
    2. Crie teste com token de usuário admin -> `assert response.status_code == 200`.
  * **Branch:** `test/auth-rbac-permissions`
  * **Commit:** `test(auth): adiciona testes de autorizacao RBAC para perfis cliente e admin`

---

### Tarefas do Frontend

#### 📋 **TSK-207: Telas Frontend de Autenticação**

* - [ ] **SUB-207.1: Construir Formulário de Login (`LoginPage.jsx`)**
  * **Descrição:** Desenvolver a página visual de Login com validação de campos.
  * **Como realizar:**
    1. Crie `src/pages/LoginPage.jsx`.
    2. Adicione os campos de entrada (E-mail e Senha) com estado reativo (`useState`).
    3. Adicione o botão "Entrar", tratamento de estado de carregamento (`loading`) e exibição de mensagem de erro.
  * **Branch:** `feature/frontend-login-page`
  * **Commit:** `feat(frontend): cria pagina e formulario de login`

* - [ ] **SUB-207.2: Construir Formulário de Cadastro (`RegisterPage.jsx`)**
  * **Descrição:** Desenvolver a página visual de registro para novos clientes.
  * **Como realizar:**
    1. Crie `src/pages/RegisterPage.jsx`.
    2. Adicione os campos: Nome, E-mail, Senha e Confirmação de Senha.
    3. Valide se a senha e a confirmação coincidem antes de disparar o envio para a API.
  * **Branch:** `feature/frontend-register-page`
  * **Commit:** `feat(frontend): cria pagina de cadastro de novos clientes`

---

#### 📋 **TSK-208: Gestão de Estado & Interceptors Frontend**

* - [ ] **SUB-208.1: Implementar `AuthContext` e Armazenamento no `localStorage`**
  * **Descrição:** Criar contexto React para manter o estado global de autenticação do usuário.
  * **Como realizar:**
    1. Crie `src/contexts/AuthContext.jsx`.
    2. Armazene o `token` e dados do `user` no `localStorage` ao efetuar login com sucesso.
    3. Exporte as funções `login(token)`, `logout()` e a variável `user` via React Context Provider.
  * **Branch:** `feature/frontend-auth-context`
  * **Commit:** `feat(frontend): cria AuthContext para gerenciamento de estado e token JWT`

* - [ ] **SUB-208.2: Interceptor Axios para Header `Authorization: Bearer` e Tratamento 401**
  * **Descrição:** Anexar o token JWT em todas as requisições protegidas e tratar a expiração de sessão.
  * **Como realizar:**
    1. Em `src/services/api.js`, adicione um interceptor de requisição para injetar `headers.Authorization = 'Bearer ' + token` quando o token existir no `localStorage`.
    2. Adicione um interceptor de resposta para interceptar status HTTP 401, limpar o `localStorage` e redirecionar para a tela de login.
  * **Branch:** `feature/frontend-axios-interceptor`
  * **Commit:** `feat(frontend): adiciona interceptor axios para injetar token JWT e tratar 401`

---

### Critérios de Aceite (DoD - Sprint 2)
1. ✅ Nenhuma senha armazenada ou retornada em texto plano.
2. ✅ Proteção funcional contra acessos não autorizados (401) e cliente tentando acessar rotas de admin (403).
3. ✅ Suíte pytest da Sprint 2 com 100% de aprovação.
