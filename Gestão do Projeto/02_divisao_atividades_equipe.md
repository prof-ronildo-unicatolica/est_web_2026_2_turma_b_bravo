# Organização da Equipe Bravo e Divisão de Papéis

**Projeto:** Sistema de Gestão Hoteleira — Estágio II (2026.2)  
**Turma:** B | **Equipe:** Bravo (7 Integrantes)

---

## 1. Integrantes da Equipe e Responsabilidades Individuais

| # | Integrante | Papel Técnico Principal | Foco Primário |
|---|---|---|---|
| 1 | **Kelvin Barros Dias** | Líder Backend / Segurança & Arquitetura | Core Service, JWT, RBAC, Motor de Precificação e Admin Frontend |
| 2 | **Paula de Freitas Mendes Barbosa** | Líder Frontend / UI & Design System | Shell de Layout, Telas de Catálogo, Vouchers e Minhas Reservas |
| 3 | **Guilherme Neves de Assis** | Backend & Banco de Dados | Conexão DB, Alembic Migrations, API de Catálogo de Hotéis |
| 4 | **Francisca Bianca da Silva** | Backend & Serviços de Domínio | Auth Service, Endpoints de Reservas, Módulo de Admin API |
| 5 | **Raul de Queiroz Moura** | DevOps & Qualidade (QA) | Infraestrutura Docker, Dependências e Suíte de Testes Automatizados |
| 6 | **Atyla Braga** | Fullstack & Telas Interativas | Telas de Login/Registro, Contexto de Auth e Checkout com Simulação |
| 7 | **Herbert Monteiro** | Backend & Frontend Integrado | Modelos de Domínio Hoteleiro, Módulo e API de Avaliações/Notas |

---

## 2. Estrutura de Papéis e Frentes de Atuação

Para garantir a autonomia e o ritmo de entregas quinzenais (Sprint Reviews), distribuímos as frentes técnicas principais entre os integrantes:

| Frente de Atuação | Responsabilidade Principal | Integrantes em Destaque | Foco Tecnológico |
| :--- | :--- | :--- | :--- |
| **Backend & Segurança** | Modelos relacionais, serviços, autenticação JWT, RBAC e testes de rota | Kelvin Barros, Francisca Bianca | FastAPI, SQLAlchemy, Alembic, Passlib/Bcrypt |
| **Frontend & UX/UI** | Telas de busca, catálogo, formulários reativos, estado global e vouchers | Paula de Freitas, Atyla Braga | React, Vite, Bootstrap, CSS Tokens, Axios |
| **Bancos de Dados & Domínio** | Modelagem PostgreSQL, migrações Alembic, modelos de domínio e avaliações | Guilherme Neves, Herbert | PostgreSQL, SQLAlchemy 2.0, Alembic, Pydantic v2 |
| **DevOps & Qualidade (QA)** | Containerização Docker, validação de PRs, suíte de testes de integração e mocks | Raul de Queiroz, Kelvin Barros | Docker Compose, Pytest, TestClient, Ruff |

---

## 3. Matriz RACI Básica das Sprints

* **R (Responsible / Responsável)**: Quem executa a tarefa.
* **A (Accountable / Aprovador)**: Quem responde pelo resultado (Lead da Frente / Revisor).
* **C (Consulted / Consultado)**: Quem apoia com conhecimento técnico.
* **I (Informed / Informado)**: Quem é notificado sobre a entrega.

| Tarefa Macro | Kelvin | Paula | Guilherme | Bianca | Raul | Atyla | Herbert |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Setup de Docker & Dependências** | C | I | I | I | **A / R** | C | I |
| **Conexão de Banco & Migrações Iniciais** | C | I | **A / R** | C | I | I | C |
| **Layout Shell & Design System CSS** | C | **A / R** | I | I | I | C | I |
| **Modelos de Usuário & Segurança JWT** | **A / R** | I | C | C | I | I | C |
| **Auth Service, RBAC & Endpoints Auth** | C | I | I | **A / R** | I | C | I |
| **Telas de Login & Cadastro (Frontend)** | I | C | I | I | I | **A / R** | I |
| **Suíte de Testes Automatizados (Pytest)** | C | I | I | I | **A / R** | C | I |
| **Modelos ORM do Domínio Hoteleiro** | C | I | C | C | I | I | **A / R** |
| **API de Catálogo de Hotéis & Migração** | I | I | **A / R** | C | I | I | C |
| **Telas de Busca & Detalhes de Hotéis** | I | **A / R** | I | I | I | C | I |
| **Motor de Precificação Dinâmica** | **A / R** | C | C | C | I | I | I |
| **API de Gestão de Reservas** | C | I | I | **A / R** | I | I | C |
| **Tela de Checkout & Cálculo Tempo Real** | I | C | I | I | I | **A / R** | I |
| **Telas de Status, Voucher & Histórico** | I | **A / R** | I | I | I | C | I |
| **Módulo & API de Avaliações** | C | I | I | C | I | I | **A / R** |
| **API Administrativa & Registro de Rotas** | C | I | I | **A / R** | C | I | I |
| **Painel Administrativo Frontend** | **A / R** | C | I | I | I | C | I |
| **Revisão e Merge de Pull Requests** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |
