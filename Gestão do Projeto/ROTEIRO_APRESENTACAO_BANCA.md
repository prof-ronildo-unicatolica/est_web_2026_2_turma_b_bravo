# 🎯 Roteiro Oficial de Apresentação para a Banca Avaliadora

**Projeto:** StayFlow — Sistema de Gestão de Rede Hoteleira e Reservas  
**Disciplina:** Estágio II em Desenvolvimento Web (2026.2) — Turma B  
**Equipe:** Bravo (7 Integrantes)  
**Professor Responsável:** Prof. Ronildo Silva  
**Data da Apresentação:** _Conforme cronograma da banca_  
**Tempo Estimado:** 20 minutos (15 min de apresentação + 5 min de arguição)

---

## 📌 1. Resumo Executivo e Escopo do Sistema

O **StayFlow** é uma solução web *full stack* corporativa para gestão distribuída de redes hoteleiras e experiência do hóspede, concebida ao longo de 8 Sprints de desenvolvimento ágil com entregas incrementais.

A plataforma implementa uma arquitetura orientada a serviços em **Monorepo**, combinando:
* **Frontend SPA:** React 18 + Vite + Bootstrap 5 + CSS Custom Tokens.
* **Backend API Gateway & Core:** FastAPI (Python 3.10/3.12) + SQLAlchemy 2.0 ORM + Pydantic v2 + Alembic.
* **Persistência Poliglota:**
  * **PostgreSQL:** Transações relacionais consistentes (Cidades, Hotéis, Quartos, Reservas, Tarifas e Usuários).
  * **MongoDB:** Persistência NoSQL orientada a documentos para trilhas de auditoria assíncrona.
* **Mensageria Assíncrona Distribuída:** Broker **RabbitMQ** com filas duráveis (`audit.logs`) consumidas por Worker assíncrono Python (`aio-pika`).
* **Qualidade e Confiabilidade:** Correções e refatorações aplicadas nos 5 eixos do SonarQube (Confiabilidade, Manutenibilidade, Complexidade, Razão de Testes RNFO07 e Segurança), visando elevação para **Rating A** (aguardando reanálise da banca).
* **CI/CD Automatizado:** Pipeline de integração contínua via **GitHub Actions** com Ruff, ESLint e Pytest.
* **Orquestração e Contêineres:** **Docker Compose** orquestrando toda a infraestrutura e microsserviços.

---

## 👥 2. Equipe Bravo e Frentes de Atuação

| # | Integrante | Papel Técnico Principal | Foco Primário na Apresentação |
|---|---|---|---|
| 1 | **Kelvin Barros Dias** | Líder Backend & Segurança | Arquitetura Core, Autenticação JWT, Guards RBAC e Endpoints Admin |
| 2 | **Paula de Freitas Mendes** | Líder Frontend & UI/UX | Design System, Shell de Layout, Catálogo de Hotéis e Experiência do Hóspede |
| 3 | **Guilherme Neves de Assis** | Backend & Banco de Dados | Modelagem Relacional, Migrações Alembic, Catálogo e Mensageria RabbitMQ |
| 4 | **Francisca Bianca da Silva** | Backend & Serviços de Domínio | Módulo de Reservas, Tratamento de Exceções HTTP e Regras de Negócio |
| 5 | **Raul de Queiroz Moura** | DevOps & Qualidade (QA) | Pipeline GitHub Actions, Hardening Docker e Suíte de Testes Automatizados |
| 6 | **Atyla Braga** | Fullstack & Telas Interativas | Fluxo de Checkout Dinâmico, Telas de Login/Registro e Logs NoSQL Admin |
| 7 | **Herbert Monteiro** | Backend & Frontend Integrado | Motor de Precificação Sazonal, Módulo de Avaliações/Notas e Seed Demo |

---

## ⏱️ 3. Roteiro Cronometrado da Apresentação (20 Minutos)

### 🔹 Bloco 1 — Abertura e Contexto do Projeto (3 minutos)
1. **Apresentação da Equipe:** Introdução dos 7 integrantes e seus papéis na entrega.
2. **Desafio de Negócio:** Centralizar a gestão de acomodações hoteleiras em múltiplos destinos com cálculo dinâmico de diárias, comodidades e transparência na auditoria.
3. **Escopo Entregue:** Apresentar a linha do tempo das 8 Sprints cumpridas (Fundação, Auth, Catálogo, Reservas, Vouchers, Painel Admin, Mensageria/CI e Suíte E2E).

---

### 🔹 Bloco 2 — Arquitetura Técnica & Engenharia de Software (4 minutos)
1. **Visão Macro da Arquitetura:**
   * Comunicação HTTP/REST entre SPA React e API FastAPI.
   * Transações ACID no PostgreSQL com ORM SQLAlchemy e migrações versionadas no Alembic.
   * Desacoplamento assíncrono: publicação de eventos de reserva no RabbitMQ sem onerar o tempo de resposta do cliente.
   * Persistência de auditoria em MongoDB via `audit_worker.py`.
2. **Segurança & RBAC:**
   * Criptografia de senhas com `passlib[bcrypt]`.
   * Tokens JWT com tempo de expiração e claims de perfil.
   * Injeção de dependências FastAPI (`get_current_user`, `get_current_admin` com HTTP 403 Forbidden para não-administradores).
3. **Pipeline de Integração Contínua (CI/CD):**
   * Validação a cada Pull Request no GitHub Actions: Linter Ruff, Pytest com banco em memória, ESLint e Vite Build com Quality Gate bloqueante.

---

### 🔹 Bloco 3 — Demonstração Prática ao Vivo (8 minutos)

#### A. Jornada do Hóspede (Cliente)
1. **Autocadastro e Autenticação:**
   * Acessar `/register` e cadastrar um novo usuário.
   * Realizar login em `/login` e demonstrar a persistência da sessão no `AuthContext` via token JWT.
2. **Navegação e Busca de Hotéis:**
   * Na Home (`/`), demonstrar a listagem de hotéis por cidade (ex: Fortaleza, Jericoacoara, Guaramiranga, Quixadá) e filtros por estrelas.
3. **Detalhes da Acomodação & Quartos:**
   * Acessar `/hoteis/:id` e exibir comodidades, galeria de fotos reais, avaliações dos hóspedes e lista de quartos.
4. **Checkout com Precificação Dinâmica:**
   * Selecionar um quarto e entrar em `/checkout/:quartoId`.
   * Demonstrar a simulação de tarifas em tempo real alterando datas de check-in/check-out e adicionando serviços extras (café da manhã, estacionamento, pet friendly).
   * Confirmar a reserva.
5. **Voucher Digital & Minhas Reservas:**
   * Visualizar a tela de confirmação (`/reserva/:id`) com código localizador e QR Code simulado.
   * Acessar `/minhas-reservas` demonstrando o histórico do cliente e a opção de cancelamento de reserva.

#### B. Jornada do Administrador
1. **Acesso com Privilégios Elevados:**
   * Login com a conta master: `admin@hotel.com` / `admin123`.
2. **Dashboard Gerencial:**
   * Acessar `/admin` e exibir métricas consolidadas: total de reservas, taxa de ocupação, faturamento bruto e gráficos dinâmicos.
3. **Auditoria NoSQL em Tempo Real:**
   * Acessar a aba de **Logs de Auditoria NoSQL**, comprovando os eventos disparados no fluxo de checkout (reserva criada, confirmada ou cancelada) persistidos no MongoDB via RabbitMQ.
4. **Catálogo & Gestão Administrativa:**
   * Visualização de cidades, hotéis e quartos cadastrados na base.

#### C. Documentação Interativa da API
* Abrir `http://localhost:8000/docs` e demonstrar a documentação OpenAPI/Swagger completa, com todos os modelos, rotas versionadas e códigos de status HTTP documentados (`200`, `201`, `400`, `401`, `403`, `404`, `409`).

---

### 🔹 Bloco 4 — Padrões de Qualidade e SonarQube (3 minutos)
1. **Plano de Ajustes de Qualidade (7 Integrantes):**
   * Apresentar as correções implementadas para os 5 relatórios de inconformidade, visando atingir o Rating A:
     * **Confiabilidade:** Eliminação de `datetime.utcnow()` legado no backend, repasse correto de `asyncio.CancelledError` no worker de auditoria e botões HTML com `type` explícito no frontend.
     * **Manutenibilidade:** Padronização e documentação de todas as exceções HTTP no Swagger (`responses={400: ..., 404: ...}`) e centralização de constantes literais.
     * **Complexidade Cognitiva:** Modularização de componentes JSX (`AdminDashboard`, `CheckoutPage`, `HotelDetailPage`) e decomposição da inicialização do banco de dados.
     * **Testes Automatizados:** Cumprimento da razão de testes e do requisito **RNFO07** (mínimo de 70% de cobertura na camada de serviços do backend, com gate automatizado no CI).
     * **Segurança:** Hardening do Dockerfile (cópias direcionadas de contexto), criação de `.dockerignore` dedicado para exclusão de arquivos sensíveis e parametrização de variáveis via `.env.exemplo`.
2. **Governança Git:**
   * Anel fechado de Code Review entre os 7 integrantes, 100% de conformidade com Conventional Commits e zero commits diretos na `main` ou `develop`.

---

### 🔹 Bloco 5 — Conclusão e Considerações Finais (2 minutos)
1. **Síntese dos Resultados:** Todas as 8 Sprints e critérios de aceite entregues com estabilidade total da stack.
2. **Desafios Superados:** Integração poliglota (SQL + NoSQL + Mensageria) e manutenção de cobertura de testes em equipe de 7 colaboradores.
3. **Abertura para Perguntas da Banca Avaliadora.**

---

## 💻 4. Guia Rápido de Execução da Stack para a Banca

Para inicializar a aplicação limpa e populada no ambiente de demonstração:

```bash
# 1. Garantir que a branch develop está atualizada
git checkout develop
git pull origin develop

# 2. Subir a stack completa com Docker Compose
docker compose up -d --build

# 3. Executar as migrações relacionais no PostgreSQL
docker compose exec core-service alembic upgrade head

# 4. Executar a carga de dados realista (Seed Demo da Banca)
docker compose exec core-service python -m app.db.seed_demo
```

### URLs e Portas de Acesso

| Serviço | URL | Credenciais / Notas |
|---|---|---|
| **Frontend Web (React)** | [http://localhost:5173](http://localhost:5173) | Interface principal do sistema |
| **API Backend + Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Documentação interativa da API |
| **RabbitMQ Management Dashboard** | [http://localhost:15672](http://localhost:15672) | Usuário: `guest` / Senha: `guest` |
| **PostgreSQL Database** | `localhost:5432` | Banco relacional `hotel_db_dev` |
| **MongoDB NoSQL** | `localhost:27017` | Coleções `logs_auditoria` e catálogo |

### Credenciais Padrão de Demonstração

| Perfil | E-mail | Senha | Nível de Permissão |
|---|---|---|---|
| **Administrador Master** | `admin@hotel.com` | `admin123` | Acesso total ao Dashboard, Logs e Catálogo (RBAC Admin) |
| **Hóspede / Cliente** | _(Cadastre um novo hóspede na tela de registro ou utilize os usuários do seed)_ | Livre | Acesso ao Catálogo, Checkout, Vouchers e Minhas Reservas |

---

## 📈 5. Quadro Geral de Métricas do Projeto

| Métrica | Valor Consolidado |
|---|---|
| **Sprints Executadas** | **8 de 8 (100% Concluído)** |
| **Integrantes com Contribuições Ativas** | **7 de 7 (100% Equidade)** |
| **Pull Requests Revisados e Mesclados** | **38 Pull Requests** (e PR #69 em revisão) |
| **Plano de Qualidade SonarQube** | **Correções nos 5 eixos aplicadas** (visando Rating A / aguardando reanálise) |
| **Cobertura da Camada de Serviços** | **≥ 70% (Requisito RNFO07 Atendido)** |
| **Pipeline de CI/CD** | **GitHub Actions Automatizado e 100% Verde** |

