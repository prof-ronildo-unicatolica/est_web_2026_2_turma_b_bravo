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

## 3. Matriz RACI Básica das Sprints (Sprints 1 a 8)

* **R (Responsible / Responsável)**: Quem executa a tarefa.
* **A (Accountable / Aprovador)**: Quem responde pelo resultado (Lead da Frente / Revisor).
* **C (Consulted / Consultado)**: Quem apoia com conhecimento técnico.
* **I (Informed / Informado)**: Quem é notificado sobre a entrega.

> **⚠️ AVISO DE CRONOGRAMA REVISADO:** Conclusão de todas as tarefas até a **Sprint 8** estipulada para **25/09/2026 às 23:59**.

| Tarefa Macro (Sprint) | Kelvin | Paula | Guilherme | Bianca | Raul | Atyla | Herbert |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Setup de Docker & Dependências (S1)** | C | I | I | I | **A / R** | C | I |
| **Conexão de Banco & Migrações Iniciais (S1)** | C | I | **A / R** | C | I | I | C |
| **Layout Shell & Design System CSS (S1)** | C | **A / R** | I | I | I | C | I |
| **Modelos de Usuário & Segurança JWT (S2)** | **A / R** | I | C | C | I | I | C |
| **Auth Service, RBAC & Endpoints Auth (S2)** | C | I | I | **A / R** | I | C | I |
| **Telas de Login & Cadastro (Frontend) (S2)** | I | C | I | I | I | **A / R** | I |
| **Suíte de Testes Automatizados (Pytest) (S2)** | C | I | I | I | **A / R** | C | I |
| **Modelos ORM do Domínio Hoteleiro (S3)** | C | I | C | C | I | I | **A / R** |
| **API de Catálogo de Hotéis & Migração (S3)** | I | I | **A / R** | C | I | I | C |
| **Telas de Busca & Detalhes de Hotéis (S3)** | I | **A / R** | I | I | I | C | I |
| **Motor de Precificação Dinâmica (S4)** | **A / R** | C | C | C | I | I | I |
| **API de Gestão de Reservas (S4)** | C | I | I | **A / R** | I | I | C |
| **Tela de Checkout & Cálculo Tempo Real (S4)** | I | C | I | I | I | **A / R** | I |
| **Telas de Status, Voucher & Histórico (S5)** | I | **A / R** | I | I | I | C | I |
| **Módulo & API de Avaliações (S5)** | C | I | I | C | I | I | **A / R** |
| **API Administrativa & Registro de Rotas (S6)** | C | I | I | **A / R** | C | I | I |
| **Painel Administrativo Frontend (S6)** | **A / R** | C | I | I | I | C | I |
| **Pipeline CI/CD Automatizado no GitHub Actions (S7)** | **A** | I | I | I | **R** | I | I |
| **Mensageria RabbitMQ & Worker MongoDB (S7)** | C | I | **R** | **A** | I | I | C |
| **Endpoint & Visualizador Logs Auditoria NoSQL (S7)** | I | **A** | I | I | I | **R** | I |
| **Suíte de Testes E2E do Domínio Hoteleiro (S8)** | C | I | I | I | **R** | **A** | I |
| **Carga de Dados Realista (Seed Demo da Banca) (S8)** | C | I | **A** | I | I | I | **R** |
| **Polimento UI/UX, Toasts & Estados Visuais (S8)** | **A** | **R** | I | I | I | C | I |
| **Orquestração de Release Final e Tag v1.0.0 (S8)** | **R** | I | I | **R** | **A** | I | I |
| **Revisão e Aprovação de Pull Requests** | **R** | **R** | **R** | **R** | **R** | **R** | **R** |

---

## 4. Balanço Geral de Contribuição (24 Entregas - 7 Integrantes)

| Integrante | PRs Como Autor | PRs Como Revisor | Frentes de Atuação nas Sprints 7 e 8 |
|---|:---:|:---:|---|
| **Kelvin Barros Dias** | **4** | **4** | Release Final v1.0.0, Revisão de CI/CD e Revisão de UX |
| **Paula de Freitas Mendes Barbosa** | **4** | **4** | Polimento de UI/UX, Toasts, Skeletons e Revisão de Auditoria |
| **Guilherme Neves de Assis** | **3** | **4** | Mensageria RabbitMQ + Worker MongoDB e Revisão de Seed Demo |
| **Francisca Bianca da Silva** | **4** | **3** | Orquestração da Release Final e Revisão de Mensageria |
| **Raul de Queiroz Moura** | **4** | **4** | Pipeline CI/CD GitHub Actions, Testes de Domínio e Revisão Release |
| **Atyla Braga** | **3** | **3** | Visualizador de Logs NoSQL no Admin e Revisão de Testes E2E |
| **Herbert Monteiro** | **3** | **3** | Script de Carga/Seed Completo da Banca e Revisões |

