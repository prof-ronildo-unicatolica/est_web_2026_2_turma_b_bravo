# ⚡ Plano Emergencial de Execução — Sprints 7 e 8 (Equipe Bravo)

**Projeto:** Sistema de Gestão Hoteleira e Reservas (StayFlow)  
**Disciplina:** Estágio II em Desenvolvimento Web — Semestre 2026.2 (Turma B)  
**Professor Responsável:** Prof. Ronildo  
**Data de Emissão:** 24/09/2026  
**⏰ Prazo Final Impreterível de Entrega:** **25/09/2026 às 23:59**  
**Repositório Oficial:** [prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo](https://github.com/prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo)  
**Branch Base de Integração:** `develop`  

---

## 🎯 1. Contexto e Motivação da Atualização

Por alinhamento do cronograma da disciplina, o ciclo de desenvolvimento foi expandido para contemplar **8 Sprints completas**, com entrega final e consolidação de código até **amanhã (25/09/2026) às 23:59**.

As **Sprints 1 a 6** cobriram a fundação, autenticação JWT/RBAC, catálogo de hotéis, motor de reservas, vouchers/avaliações e painel administrativo.  
As **Sprints 7 e 8** chegam para fechar as exigências arquiteturais avançadas do sistema:
1. **Sprint 7**: Mensageria assíncrona com RabbitMQ, persistência de auditoria NoSQL no MongoDB e automação de CI/CD no GitHub Actions.
2. **Sprint 8**: Suíte abrangente de testes de integração (QA), script de carga de dados realista (Seed Demo) para avaliação da banca, polimento estético/UX e orquestração da Release Final `v1.0.0` para a branch `main`.

---

## 👥 2. Matriz de Distribuição entre os 7 Integrantes

A distribuição foi calibrada para manter total equidade de contribuição (critério de avaliação de estágio):

| # | Integrante | Papel Principal | Tarefa na Sprint 7 | Tarefa na Sprint 8 |
|---|---|---|---|---|
| 1 | **Kelvin Barros Dias** | Líder Backend & Segurança | Revisa Tarefa 7.1 | **Tarefa 8.4:** Release v1.0.0 & Banca |
| 2 | **Paula de Freitas Mendes** | Líder Frontend & UI/UX | Revisa Tarefa 7.3 | **Tarefa 8.3:** Polimento UI/UX & Toasts |
| 3 | **Guilherme Neves de Assis** | Backend & Banco de Dados | **Tarefa 7.2:** RabbitMQ + MongoDB | Revisa Tarefa 8.2 |
| 4 | **Francisca Bianca da Silva** | Backend & Serviços | Revisa Tarefa 7.2 | **Tarefa 8.4:** Roteiro da Banca & Release |
| 5 | **Raul de Queiroz Moura** | DevOps & Qualidade (QA) | **Tarefa 7.1:** Pipeline CI/CD Actions | **Tarefa 8.1:** Suíte Testes E2E Domínio |
| 6 | **Atyla Braga** | Fullstack & Telas | **Tarefa 7.3:** Logs NoSQL no Admin | Revisa Tarefa 8.1 |
| 7 | **Herbert Monteiro** | Backend & Modelos | Revisa Tarefa 7.3 (apoio) | **Tarefa 8.2:** Seed Completo da Banca |

---

## 📋 3. Detalhamento Técnico das Tarefas

### ⚡ SPRINT 7 — Mensageria Assíncrona, Auditoria NoSQL & CI/CD Pipeline

#### 📌 Tarefa 7.1 — Pipeline de CI/CD Automatizado no GitHub Actions
* **Responsável:** **Raul de Queiroz Moura** | **Revisor:** **Kelvin Barros Dias**
* **Branch:** `chore/ci-github-actions`
* **Objetivo:** Criar `.github/workflows/ci.yml` para rodar linter Ruff, testes Pytest e build do frontend automaticamente em cada PR para a branch `develop`.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/ci-github-actions
  git add .github/workflows/ci.yml
  git commit -m "chore(ci): implementa pipeline automatizado de testes e lint no github actions"
  git push -u origin chore/ci-github-actions
  ```
* **Título do PR:** `[Sprint 7] Chore: Pipeline de CI/CD automatizado no GitHub Actions`

#### 📌 Tarefa 7.2 — Publicação e Consumo de Eventos de Auditoria no RabbitMQ & MongoDB
* **Responsável:** **Guilherme Neves de Assis** | **Revisora:** **Francisca Bianca da Silva**
* **Branch:** `feature/rabbitmq-audit-worker`
* **Objetivo:** Conectar a publicação de eventos assíncronos (`audit.logs`) na criação e cancelamento de reservas e validar a gravação no MongoDB pelo `audit_worker.py`.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/rabbitmq-audit-worker
  git add apps/services/core-service/app/workers/audit_worker.py apps/services/core-service/app/core/rabbitmq.py
  git commit -m "feat(worker): conecta publicacao e consumo de eventos assincronos com rabbitmq e mongodb"
  git push -u origin feature/rabbitmq-audit-worker
  ```
* **Título do PR:** `[Sprint 7] Feat: Mensageria assíncrona com RabbitMQ e Worker MongoDB`

#### 📌 Tarefa 7.3 — Endpoint e Visualizador de Logs de Auditoria NoSQL no Painel Admin
* **Responsável:** **Atyla Braga** | **Revisora:** **Paula de Freitas Mendes**
* **Branch:** `feature/admin-audit-logs-view`
* **Objetivo:** Criar endpoint `GET /api/v1/admin/logs` para consulta das mensagens salvas no MongoDB e adicionar a aba de Auditoria NoSQL no `AdminDashboard.jsx`.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/admin-audit-logs-view
  git add apps/services/core-service/app/api/v1/admin.py apps/frontend/src/pages/admin/AdminDashboard.jsx
  git commit -m "feat(admin): implementa consulta e aba visual de logs de auditoria assincronos"
  git push -u origin feature/admin-audit-logs-view
  ```
* **Título do PR:** `[Sprint 7] Feat: Endpoint e tela de logs de auditoria no painel administrativo`

---

### 🏆 SPRINT 8 — Suíte de Testes E2E, Seed Completo da Banca & Release Final v1.0.0

#### 📌 Tarefa 8.1 — Suíte Abrangente de Testes de Integração do Domínio e Relatório de Cobertura
* **Responsável:** **Raul de Queiroz Moura** | **Revisor:** **Atyla Braga**
* **Branch:** `test/domain-integration-suite`
* **Objetivo:** Implementar testes automatizados cobrindo rotas de hotéis, reservas, precificação sazonal e cancelamentos em `tests/test_hoteis.py` e `tests/test_reservas.py`.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b test/domain-integration-suite
  git add apps/services/core-service/tests/test_hoteis.py apps/services/core-service/tests/test_reservas.py
  git commit -m "test(qa): implementa suite de testes de integracao para hoteis, calculo de reservas e cancelamento"
  git push -u origin test/domain-integration-suite
  ```
* **Título do PR:** `[Sprint 8] Test: Suíte completa de testes de integração para o domínio hoteleiro`

#### 📌 Tarefa 8.2 — Script de Carga de Dados Realista (Seed Completo da Banca)
* **Responsável:** **Herbert Monteiro** | **Revisor:** **Guilherme Neves de Assis**
* **Branch:** `feature/seed-catalog-demo`
* **Objetivo:** Criar `app/db/seed_demo.py` com hotéis, fotos de alta qualidade, comodidades reais e histórico de reservas para visualização rica na banca.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/seed-catalog-demo
  git add apps/services/core-service/app/db/seed_demo.py
  git commit -m "feat(db): adiciona script de seed completo com cidades, hoteis, quartos e reservas para demonstracao"
  git push -u origin feature/seed-catalog-demo
  ```
* **Título do PR:** `[Sprint 8] Feat: Script de seed de dados completo para demonstração e banca`

#### 📌 Tarefa 8.3 — Polimento de UI/UX, Feedback Visual (Toasts/Loading) e Tratamento de Erros
* **Responsável:** **Paula de Freitas Mendes** | **Revisor:** **Kelvin Barros Dias**
* **Branch:** `feature/frontend-ux-polish`
* **Objetivo:** Adicionar feedback visual com toasts, animações de carregamento (skeletons/spinners) e tratamento de erros 404/500 na SPA React.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-ux-polish
  git add apps/frontend/src/components/common/Toast.jsx apps/frontend/src/custom.css
  git commit -m "feat(frontend): adiciona feedback visual de toasts, skeletons e polimento de UI"
  git push -u origin feature/frontend-ux-polish
  ```
* **Título do PR:** `[Sprint 8] Feat: Polimento visual de UI/UX, toasts e estados de carregamento`

#### 📌 Tarefa 8.4 — Orquestração de Release Final, Roteiro da Banca e Tag v1.0.0
* **Responsáveis:** **Kelvin Barros Dias** e **Francisca Bianca da Silva** | **Revisor:** **Raul de Queiroz Moura**
* **Branch:** `chore/release-v1.0.0-prep`
* **Objetivo:** Elaborar o roteiro oficial de apresentação da banca (`ROTEIRO_APRESENTACAO_BANCA.md`) e preparar o Pull Request final da branch `develop` para a branch `main` com tag `v1.0.0`.
* **Comandos:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/release-v1.0.0-prep
  git add "Gestão do Projeto/ROTEIRO_APRESENTACAO_BANCA.md" README.md
  git commit -m "chore(release): prepara roteiro da banca avaliadora e orquestracao final v1.0.0"
  git push -u origin chore/release-v1.0.0-prep
  ```
* **Título do PR:** `[Sprint 8] Chore: Orquestração de entrega final e release v1.0.0 para branch main`

---

## 🔄 4. Ciclo de Revisão e Aprovação de PRs

Para cada PR aberto:
1. O autor envia o link no grupo da equipe.
2. O revisor designado entra na aba **Pull requests** no GitHub.
3. Clica em **Files changed**, faz a revisão e clica em **Review changes ➔ Approve**.
4. Clica em **Merge pull request ➔ Confirm merge**.
5. O revisor avisa no grupo para que o próximo integrante faça o `git checkout develop && git pull origin develop`.

---

## ☁️ 5. Instruções para Compartilhamento no Google Drive

Para disponibilizar este documento atualizado a todos no Google Drive:
1. Este arquivo está salvo no repositório em:  
   `Gestão do Projeto/PLANO_EMERGENCIAL_SPRINTS_7_E_8.md`.
2. Para subir no Drive da turma:
   * Abra a pasta compartilhada no Google Drive.
   * Clique em **Novo (+) ➔ Fazer upload de arquivo**.
   * Selecione este arquivo (`PLANO_EMERGENCIAL_SPRINTS_7_E_8.md`) ou abra-o, copie todo o texto e cole em um novo **Documento Google** com o título:  
     `Plano Emergencial — Sprints 7 e 8 — Equipe Bravo`.
   * Compartilhe o link do Google Docs com permissão de visualização para a turma e o professor.
