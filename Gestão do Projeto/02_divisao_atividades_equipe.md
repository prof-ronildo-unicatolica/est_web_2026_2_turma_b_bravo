# Organização da Equipe Bravo e Divisão de Papéis

**Projeto:** Sistema de Gestão Hoteleira — Estágio II (2026.2)  
**Turma:** B | **Equipe:** Bravo  

---

## 1. Integrantes da Equipe

1. **Kelvin Barros Dias**
2. **Paula de Freitas Mendes Barbosa**
3. **Guilherme Neves de Assis**
4. **Francisca Bianca da Silva**
5. **Raul de Queiroz Moura**

---

## 2. Estrutura de Papéis e Frentes de Atuação

Para garantir a autonomia e o ritmo de entregas quinzenais (Sprint Reviews), distribuímos as frentes técnicas principais entre os integrantes:

| Frente de Atuação | Responsabilidade Principal | Foco Técnico |
| :--- | :--- | :--- |
| **Backend & Segurança** | Modelos relacionais, serviços, autenticação JWT, RBAC e testes de rota | FastAPI, SQLAlchemy, Alembic, Pytest |
| **Frontend & UX/UI** | Telas do cliente/admin, formulários reativos, estado global e integração HTTP | React, Vite, Bootstrap, Axios/Fetch |
| **Bancos de Dados & Mensageria** | Modelagem PostgreSQL, NoSQL MongoDB (CQRS/Auditoria) e Filas | PostgreSQL, MongoDB (Motor), RabbitMQ |
| **DevOps & Qualidade (QA)** | Containerização Docker, validação de PRs, suíte de testes e linting | Docker Compose, Pytest, ESLint, Ruff |

---

## 3. Matriz RACI Básica das Sprints 1 e 2

* **R (Responsible / Responsável)**: Quem executa a tarefa.
* **A (Accountable / Aprovador)**: Quem responde pelo resultado (Lead da Frente).
* **C (Consulted / Consultado)**: Quem apoia com conhecimento técnico.
* **I (Informed / Informado)**: Quem é notificado sobre a entrega.

| Tarefa Macro | Backend Lead | Frontend Lead | DB/DevOps Lead | QA Lead |
| :--- | :---: | :---: | :---: | :---: |
| **Setup de Docker & Bancos** | C | I | **A / R** | C |
| **Models SQL & Migrações Alembic** | **A / R** | I | C | C |
| **Módulo de Autenticação JWT (Sprint 2)** | **A / R** | C | C | C |
| **Telas de Login / Cadastro (Sprint 2)** | C | **A / R** | I | C |
| **Suíte de Testes Automatizados (Pytest)** | C | I | I | **A / R** |
| **Revisão e Merge de Pull Requests** | **R** | **R** | **R** | **R** |
