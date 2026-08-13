# Regras do Projeto — Estágio II (Equipe Bravo - 2026.2)

Este arquivo define as regras de desenvolvimento, convenções de código, versionamento e regras de arquitetura que TODOS os agentes de IA e desenvolvedores da **Equipe Bravo** devem seguir rigorosamente neste repositório.

---

## 1. Regras de Versionamento e Gitflow

* **Branch `main`**: Exclusiva para versões estáveis e entregas finais da disciplina. **Proibido push direto.**
* **Branch `develop`**: Branch padrão de desenvolvimento da equipe. **Proibido push direto** (Branch Protegida no GitHub).
* **Branches de Trabalho**:
  * Todas as branches devem ser criadas a partir da `develop`.
  * **Nomenclatura Obrigatória**:
    * `feature/<modulo>-<descricao-curta>` (ex: `feature/auth-jwt-backend`)
    * `fix/<modulo>-<descricao-bug>` (ex: `fix/cors-header-error`)
    * `docs/<descricao-curta>` (ex: `docs/estrutura-gestao-projeto`)
    * `chore/<infra-ou-config>` (ex: `chore/docker-env-config`)

---

## 2. Padronização de Commits (Conventional Commits)

Todos os commits devem seguir rigorosamente o padrão **Conventional Commits**:

* `feat(escopo): mensagem descritiva` — Nova funcionalidade.
* `fix(escopo): mensagem descritiva` — Correção de erro/bug.
* `docs(escopo): mensagem descritiva` — Alterações em documentação.
* `refactor(escopo): mensagem descritiva` — Refatoração de código.
* `test(escopo): mensagem descritiva` — Testes automatizados.
* `style(escopo): mensagem descritiva` — Formatação/estilo de código.
* `chore(escopo): mensagem descritiva` — Tarefas de build, infra ou dependências.

---

## 3. Regras de Pull Requests (PRs)

1. **Destino Obrigatório**: Todo PR deve ter como alvo a branch `develop`.
2. **Título do PR**: Deve seguir o padrão `[Sprint X] Tipo: Descrição resumida` (ex: `[Sprint 2] Feat: Implementação de autenticação JWT`).
3. **Validação**: Todo PR necessita de aprovação no Code Review antes de ser mesclado na `develop`.

---

## 4. Diretrizes Técnicas de Arquitetura

### Back-End (FastAPI + Python)
* **Estrutura**: Seguir arquitetura em camadas em `apps/backend/app/` (`models/`, `schemas/`, `api/`, `services/`, `core/`).
* **Validação**: Sempre utilizar schemas **Pydantic v2** para validação de entrada/saída de dados na API.
* **ORM e Banco**: Utilizar **SQLAlchemy 2.0** com migrations via **Alembic** para alterações no PostgreSQL.
* **Segurança**: Autenticação via tokens JWT (*Bearer Token*) com hash de senhas via `passlib[bcrypt]`.

### Front-End (React + Vite)
* **Estrutura**: Em `apps/frontend/src/` (`components/`, `pages/`, `services/`, `context/`, `hooks/`).
* **Estilização**: CSS Vanilla moderno, design limpo, responsivo e de alta qualidade estética.
* **Integração HTTP**: Centralizar chamadas de API em serviços modulares (ex: `services/api.js`).

### Containerização (Docker Compose)
* Manter o suporte a execução via `docker compose up -d --build`.
* Portas padrão: Backend `8000`, Frontend `5173`, PostgreSQL `5432`, MongoDB `27017`, RabbitMQ `15672`.
