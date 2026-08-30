# 📘 Playbook de Execução Diária — Equipe Bravo (2026.2)

**Projeto Oficial (Onde subimos as tasks/PRs):** [prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo](https://github.com/prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo)  
**Repositório Fonte (Onde os arquivos prontos ficam guardados):** [DevKelvinbd/est_web_2026_2_turma_b_bravo](https://github.com/DevKelvinbd/est_web_2026_2_turma_b_bravo)  
**Branch de Integração Oficial:** `develop`  
**Branch Fonte dos Arquivos Prontos:** `fonte/backup/stayflow-completo`  

---

## 👥 Integrantes e Ciclo de Code Review

| # | Integrante | Papel Principal | Revisa PR de quem? |
|---|---|---|---|
| 1 | **Kelvin Barros Dias** | Líder Backend / Auth / Core | ➔ Revisa PRs do **Raul** |
| 2 | **Paula de Freitas Mendes Barbosa** | Líder Frontend / UI / Telas Clientes | ➔ Revisa PRs do **Kelvin** |
| 3 | **Guilherme Neves de Assis** | Backend / Precificação / Reservas | ➔ Revisa PRs da **Paula** |
| 4 | **Francisca Bianca da Silva** | Backend / Catálogo / Schemas / Avaliações | ➔ Revisa PRs do **Guilherme** |
| 5 | **Raul de Queiroz Moura** | DevOps / Docker / Admin / Testes | ➔ Revisa PRs da **Bianca** |

---

## ⚡ Preparação Única na Máquina de Cada Aluno

Antes da primeira task, o aluno configura o repositório oficial e adiciona o repositório de download com o comando:

```bash
# 1. Clonar o repositório oficial da turma:
git clone https://github.com/prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo.git
cd est_web_2026_2_turma_b_bravo

# 2. Adicionar o repositório fonte de download dos arquivos:
git remote add fonte https://github.com/DevKelvinbd/est_web_2026_2_turma_b_bravo.git
git fetch fonte
```

---

## 🚀 Como Funciona a Execução Rápida (Zero Esforço)

Todos os arquivos do projeto já estão 100% implementados na branch de backup `fonte/backup/stayflow-completo`.  
Para cumprir cada tarefa:
1. Atualize sua branch `develop` a partir da oficial:
   ```bash
   git checkout develop && git pull origin develop
   ```
2. Crie a branch da task indicada:
   ```bash
   git checkout -b <nome-da-branch>
   ```
3. Copie o arquivo pronto diretamente do repositório fonte usando o comando:
   ```bash
   git checkout fonte/backup/stayflow-completo -- <caminho-do-arquivo>
   ```
4. Faça o `git commit` com a mensagem indicada no roteiro.
5. Dê `git push -u origin <nome-da-branch>` para enviar ao repositório oficial da turma.
6. Abra o Pull Request no GitHub da turma apontando para a `develop`.
7. O revisor indicado acessa o GitHub oficial, aprova o PR e faz o Merge.

---

## 📅 Roteiro Diário de Subida das Tarefas

```mermaid
graph TD
    D1["Dia 1: Raul<br>Dependências & Docker"] --> D2["Dia 2: Guilherme<br>Conexão Banco & Alembic"]
    D2 --> D3["Dia 3: Paula<br>Layout Shell & CSS"]
    D3 --> D4["Dia 4: Kelvin<br>Model Usuário & JWT"]
    D4 --> D5["Dia 5: Bianca<br>Auth Service & Endpoints"]
    D5 --> D6["Dia 6: Paula<br>Telas Login & Register"]
    D6 --> D7["Dia 7: Raul<br>Suíte de Testes Auth"]
    D7 --> D8["Dia 8: Bianca<br>Models Domínio Hoteleiro"]
    D8 --> D9["Dia 9: Guilherme<br>API Catálogo & Migração"]
    D9 --> D10["Dia 10: Paula<br>Telas Home & Hotel Detail"]
    D10 --> D11["Dia 11: Kelvin<br>Motor Precificação"]
    D11 --> D12["Dia 12: Bianca<br>API Reservas"]
    D12 --> D13["Dia 13: Guilherme<br>Tela Checkout"]
    D13 --> D14["Dia 14: Paula<br>Telas Status & Vouchers"]
    D14 --> D15["Dia 15: Bianca<br>API Avaliações"]
    D15 --> D16["Dia 16: Raul<br>API Admin & Main"]
    D16 --> D17["Dia 17: Kelvin<br>Painel Admin Frontend"]
```

---

### 🚀 SPRINT 1 — Fundação, Infra e Setup

---

#### 📌 Dia 1 | Tarefa 1.1 — Atualização de Dependências e Docker
* **Responsável:** **Raul de Queiroz Moura**
* **Revisor Obrigatório:** **Kelvin Barros Dias**
* **Branch:** `chore/docker-env-config`
* **Arquivos:**
  * `.gitignore`
  * `apps/services/core-service/requirements.txt`
  * `apps/services/core-service/pyproject.toml`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/docker-env-config
  git checkout fonte/backup/stayflow-completo -- .gitignore apps/services/core-service/requirements.txt apps/services/core-service/pyproject.toml
  git add .gitignore apps/services/core-service/requirements.txt apps/services/core-service/pyproject.toml
  git commit -m "chore(infra): atualiza dependencias e variaveis de ambiente da stack"
  git push -u origin chore/docker-env-config
  ```
* **Abertura do PR:**
  * **Repositório:** [prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo](https://github.com/prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo)
  * **Base:** `develop` | **Head:** `chore/docker-env-config`
  * **Título:** `[Sprint 1] Chore: Configuração de dependências e ambiente Docker`
  * **Reviewer:** Kelvin Barros Dias

---

#### 📌 Dia 2 | Tarefa 1.2 — Configuração de Conexão com Banco e Alembic
* **Responsável:** **Guilherme Neves de Assis**
* **Revisor Obrigatório:** **Francisca Bianca da Silva**
* **Branch:** `feature/db-initial-connection`
* **Arquivos:**
  * `apps/services/core-service/app/core/config.py`
  * `apps/services/core-service/alembic/env.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/db-initial-connection
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/core/config.py apps/services/core-service/alembic/env.py
  git add apps/services/core-service/app/core/config.py apps/services/core-service/alembic/env.py
  git commit -m "feat(db): configura conexao unificada sqlalchemy e alembic"
  git push -u origin feature/db-initial-connection
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/db-initial-connection`
  * **Título:** `[Sprint 1] Feat: Conexão e configuração do banco de dados e Alembic`
  * **Reviewer:** Francisca Bianca da Silva

---

#### 📌 Dia 3 | Tarefa 1.3 — Shell de Layout e Design System CSS
* **Responsável:** **Paula de Freitas Mendes Barbosa**
* **Revisor Obrigatório:** **Guilherme Neves de Assis**
* **Branch:** `feature/frontend-shell-layout`
* **Arquivos:**
  * `apps/frontend/package.json`
  * `apps/frontend/package-lock.json`
  * `apps/frontend/src/components/layout/Navbar.jsx`
  * `apps/frontend/src/components/layout/Footer.jsx`
  * `apps/frontend/src/index.css`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-shell-layout
  git checkout fonte/backup/stayflow-completo -- apps/frontend/package.json apps/frontend/package-lock.json apps/frontend/src/components/layout/Navbar.jsx apps/frontend/src/components/layout/Footer.jsx apps/frontend/src/index.css
  git add apps/frontend/package.json apps/frontend/package-lock.json apps/frontend/src/components/layout/Navbar.jsx apps/frontend/src/components/layout/Footer.jsx apps/frontend/src/index.css
  git commit -m "feat(frontend): cria componentes de layout Navbar, Footer e tokens css"
  git push -u origin feature/frontend-shell-layout
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/frontend-shell-layout`
  * **Título:** `[Sprint 1] Feat: Layout Shell e Design System CSS do Frontend`
  * **Reviewer:** Guilherme Neves de Assis

---

### 🔑 SPRINT 2 — Autenticação & Autorização JWT + RBAC

---

#### 📌 Dia 4 | Tarefa 2.1 — Modelo de Usuário, Hash Bcrypt e Segurança JWT
* **Responsável:** **Kelvin Barros Dias**
* **Revisor Obrigatório:** **Paula de Freitas Mendes Barbosa**
* **Branch:** `feature/auth-security-jwt-backend`
* **Arquivos:**
  * `apps/services/core-service/app/models/usuario.py`
  * `apps/services/core-service/app/core/security.py`
  * `apps/services/core-service/app/schemas/auth.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/auth-security-jwt-backend
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/models/usuario.py apps/services/core-service/app/core/security.py apps/services/core-service/app/schemas/auth.py
  git add apps/services/core-service/app/models/usuario.py apps/services/core-service/app/core/security.py apps/services/core-service/app/schemas/auth.py
  git commit -m "feat(auth): implementa modelo de usuario, hash bcrypt e geracao jwt"
  git push -u origin feature/auth-security-jwt-backend
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/auth-security-jwt-backend`
  * **Título:** `[Sprint 2] Feat: Modelo de Usuário, Hashing e Segurança JWT`
  * **Reviewer:** Paula de Freitas Mendes Barbosa

---

#### 📌 Dia 5 | Tarefa 2.2 — Serviço de Auth, Dependências RBAC e Endpoints
* **Responsável:** **Francisca Bianca da Silva**
* **Revisor Obrigatório:** **Raul de Queiroz Moura**
* **Branch:** `feature/auth-endpoints-service`
* **Arquivos:**
  * `apps/services/core-service/app/services/auth_service.py`
  * `apps/services/core-service/app/api/deps.py`
  * `apps/services/core-service/app/api/v1/auth.py`
  * `apps/services/core-service/app/db/__init__.py`
  * `apps/services/core-service/app/db/seed.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/auth-endpoints-service
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/services/auth_service.py apps/services/core-service/app/api/deps.py apps/services/core-service/app/api/v1/auth.py apps/services/core-service/app/db/__init__.py apps/services/core-service/app/db/seed.py
  git add apps/services/core-service/app/services/auth_service.py apps/services/core-service/app/api/deps.py apps/services/core-service/app/api/v1/auth.py apps/services/core-service/app/db/__init__.py apps/services/core-service/app/db/seed.py
  git commit -m "feat(auth): implementa servico de autenticacao, dependencias rbac e endpoints auth"
  git push -u origin feature/auth-endpoints-service
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/auth-endpoints-service`
  * **Título:** `[Sprint 2] Feat: Serviço de Autenticação, Guards RBAC e Endpoints /auth`
  * **Reviewer:** Raul de Queiroz Moura

---

#### 📌 Dia 6 | Tarefa 2.3 — Telas de Login/Registro e Contexto de Autenticação
* **Responsável:** **Paula de Freitas Mendes Barbosa**
* **Revisor Obrigatório:** **Guilherme Neves de Assis**
* **Branch:** `feature/frontend-auth-integration`
* **Arquivos:**
  * `apps/frontend/src/services/api.js`
  * `apps/frontend/src/contexts/AuthContext.jsx`
  * `apps/frontend/src/components/layout/ProtectedRoute.jsx`
  * `apps/frontend/src/pages/LoginPage.jsx`
  * `apps/frontend/src/pages/RegisterPage.jsx`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-auth-integration
  git checkout fonte/backup/stayflow-completo -- apps/frontend/src/services/api.js apps/frontend/src/contexts/AuthContext.jsx apps/frontend/src/components/layout/ProtectedRoute.jsx apps/frontend/src/pages/LoginPage.jsx apps/frontend/src/pages/RegisterPage.jsx
  git add apps/frontend/src/services/api.js apps/frontend/src/contexts/AuthContext.jsx apps/frontend/src/components/layout/ProtectedRoute.jsx apps/frontend/src/pages/LoginPage.jsx apps/frontend/src/pages/RegisterPage.jsx
  git commit -m "feat(frontend): implementa auth context, interceptor jwt e telas de login e cadastro"
  git push -u origin feature/frontend-auth-integration
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/frontend-auth-integration`
  * **Título:** `[Sprint 2] Feat: Telas de Login/Registro e Contexto de Autenticação com JWT`
  * **Reviewer:** Guilherme Neves de Assis

---

#### 📌 Dia 7 | Tarefa 2.4 — Suíte de Testes Automatizados JWT & RBAC
* **Responsável:** **Raul de Queiroz Moura**
* **Revisor Obrigatório:** **Kelvin Barros Dias**
* **Branch:** `test/auth-integration-suite`
* **Arquivos:**
  * `apps/services/core-service/tests/conftest.py`
  * `apps/services/core-service/tests/test_auth_jwt.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b test/auth-integration-suite
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/tests/conftest.py apps/services/core-service/tests/test_auth_jwt.py
  git add apps/services/core-service/tests/conftest.py apps/services/core-service/tests/test_auth_jwt.py
  git commit -m "test(auth): implementa suite de testes automatizados para fluxos jwt e rbac"
  git push -u origin test/auth-integration-suite
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `test/auth-integration-suite`
  * **Título:** `[Sprint 2] Test: Suíte de testes de integração JWT e permissões RBAC`
  * **Reviewer:** Kelvin Barros Dias

---

### 🏨 SPRINT 3 — Domínio Hoteleiro & Catálogo de Hotéis

---

#### 📌 Dia 8 | Tarefa 3.1 — Modelos ORM e Schemas Pydantic do Domínio Hoteleiro
* **Responsável:** **Francisca Bianca da Silva**
* **Revisor Obrigatório:** **Raul de Queiroz Moura**
* **Branch:** `feature/hotel-models-schemas`
* **Arquivos:**
  * `apps/services/core-service/app/models/cidade.py`
  * `apps/services/core-service/app/models/hotel.py`
  * `apps/services/core-service/app/models/comodidade.py`
  * `apps/services/core-service/app/models/quarto.py`
  * `apps/services/core-service/app/models/__init__.py`
  * `apps/services/core-service/app/schemas/hotelaria.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/hotel-models-schemas
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/models/cidade.py apps/services/core-service/app/models/hotel.py apps/services/core-service/app/models/comodidade.py apps/services/core-service/app/models/quarto.py apps/services/core-service/app/models/__init__.py apps/services/core-service/app/schemas/hotelaria.py
  git add apps/services/core-service/app/models/cidade.py apps/services/core-service/app/models/hotel.py apps/services/core-service/app/models/comodidade.py apps/services/core-service/app/models/quarto.py apps/services/core-service/app/models/__init__.py apps/services/core-service/app/schemas/hotelaria.py
  git commit -m "feat(models): implementa modelos orm e schemas pydantic para cidade, hotel, quarto e comodidades"
  git push -u origin feature/hotel-models-schemas
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/hotel-models-schemas`
  * **Título:** `[Sprint 3] Feat: Modelos SQLAlchemy e Schemas Pydantic do Domínio Hoteleiro`
  * **Reviewer:** Raul de Queiroz Moura

---

#### 📌 Dia 9 | Tarefa 3.2 — Endpoints de Catálogo e Migração Alembic
* **Responsável:** **Guilherme Neves de Assis**
* **Revisor Obrigatório:** **Francisca Bianca da Silva**
* **Branch:** `feature/hotel-catalog-api`
* **Arquivos:**
  * `apps/services/core-service/app/api/v1/hoteis.py`
  * `apps/services/core-service/alembic/versions/f519176e1f37_add_stayflow_domain_models.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/hotel-catalog-api
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/api/v1/hoteis.py apps/services/core-service/alembic/versions/f519176e1f37_add_stayflow_domain_models.py
  git add apps/services/core-service/app/api/v1/hoteis.py apps/services/core-service/alembic/versions/f519176e1f37_add_stayflow_domain_models.py
  git commit -m "feat(api): implementa endpoints de busca e catalogo de hoteis e migracao alembic"
  git push -u origin feature/hotel-catalog-api
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/hotel-catalog-api`
  * **Título:** `[Sprint 3] Feat: Endpoints de Catálogo de Hotéis e Migração Alembic`
  * **Reviewer:** Francisca Bianca da Silva

---

#### 📌 Dia 10 | Tarefa 3.3 — Telas de Busca de Hotéis e Detalhes da Acomodação
* **Responsável:** **Paula de Freitas Mendes Barbosa**
* **Revisor Obrigatório:** **Guilherme Neves de Assis**
* **Branch:** `feature/frontend-hotel-catalog`
* **Arquivos:**
  * `apps/frontend/src/pages/HomePage.jsx`
  * `apps/frontend/src/pages/HotelDetailPage.jsx`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-hotel-catalog
  git checkout fonte/backup/stayflow-completo -- apps/frontend/src/pages/HomePage.jsx apps/frontend/src/pages/HotelDetailPage.jsx
  git add apps/frontend/src/pages/HomePage.jsx apps/frontend/src/pages/HotelDetailPage.jsx
  git commit -m "feat(frontend): implementa telas de home com busca de hoteis e detalhes com quartos"
  git push -u origin feature/frontend-hotel-catalog
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/frontend-hotel-catalog`
  * **Título:** `[Sprint 3] Feat: Telas de Busca de Hotéis e Detalhes da Acomodação`
  * **Reviewer:** Guilherme Neves de Assis

---

### 💳 SPRINT 4 — Motor de Reservas & Precificação Dinâmica

---

#### 📌 Dia 11 | Tarefa 4.1 — Motor de Precificação Dinâmica e Modelos de Reserva
* **Responsável:** **Kelvin Barros Dias**
* **Revisor Obrigatório:** **Paula de Freitas Mendes Barbosa**
* **Branch:** `feature/booking-pricing-engine`
* **Arquivos:**
  * `apps/services/core-service/app/models/reserva.py`
  * `apps/services/core-service/app/models/tarifa_temporada.py`
  * `apps/services/core-service/app/models/servico_adicional.py`
  * `apps/services/core-service/app/services/pricing_service.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/booking-pricing-engine
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/models/reserva.py apps/services/core-service/app/models/tarifa_temporada.py apps/services/core-service/app/models/servico_adicional.py apps/services/core-service/app/services/pricing_service.py
  git add apps/services/core-service/app/models/reserva.py apps/services/core-service/app/models/tarifa_temporada.py apps/services/core-service/app/models/servico_adicional.py apps/services/core-service/app/services/pricing_service.py
  git commit -m "feat(pricing): implementa modelos de reservas e temporadas com motor de precificacao dinamica"
  git push -u origin feature/booking-pricing-engine
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/booking-pricing-engine`
  * **Título:** `[Sprint 4] Feat: Motor de Precificação Dinâmica e Modelos de Reserva`
  * **Reviewer:** Paula de Freitas Mendes Barbosa

---

#### 📌 Dia 12 | Tarefa 4.2 — Endpoints REST para Criação e Gestão de Reservas
* **Responsável:** **Francisca Bianca da Silva**
* **Revisor Obrigatório:** **Raul de Queiroz Moura**
* **Branch:** `feature/booking-api-endpoints`
* **Arquivos:**
  * `apps/services/core-service/app/api/v1/reservas.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/booking-api-endpoints
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/api/v1/reservas.py
  git add apps/services/core-service/app/api/v1/reservas.py
  git commit -m "feat(api): implementa endpoints de criacao, simulacao e cancelamento de reservas"
  git push -u origin feature/booking-api-endpoints
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/booking-api-endpoints`
  * **Título:** `[Sprint 4] Feat: Endpoints REST para Criação e Gestão de Reservas`
  * **Reviewer:** Raul de Queiroz Moura

---

#### 📌 Dia 13 | Tarefa 4.3 — Tela de Checkout com Simulação em Tempo Real
* **Responsável:** **Guilherme Neves de Assis**
* **Revisor Obrigatório:** **Francisca Bianca da Silva**
* **Branch:** `feature/frontend-checkout-booking`
* **Arquivos:**
  * `apps/frontend/src/pages/CheckoutPage.jsx`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-checkout-booking
  git checkout fonte/backup/stayflow-completo -- apps/frontend/src/pages/CheckoutPage.jsx
  git add apps/frontend/src/pages/CheckoutPage.jsx
  git commit -m "feat(frontend): implementa tela de checkout com calculo em tempo real e servicos adicionais"
  git push -u origin feature/frontend-checkout-booking
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/frontend-checkout-booking`
  * **Título:** `[Sprint 4] Feat: Tela de Checkout Interativo com Cálculo em Tempo Real`
  * **Reviewer:** Francisca Bianca da Silva

---

### 🎫 SPRINT 5 — Vouchers, Minhas Reservas & Avaliações

---

#### 📌 Dia 14 | Tarefa 5.1 — Telas de Status de Reserva, Voucher e Histórico
* **Responsável:** **Paula de Freitas Mendes Barbosa**
* **Revisor Obrigatório:** **Guilherme Neves de Assis**
* **Branch:** `feature/frontend-booking-status-voucher`
* **Arquivos:**
  * `apps/frontend/src/pages/BookingStatusPage.jsx`
  * `apps/frontend/src/pages/MyBookingsPage.jsx`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/frontend-booking-status-voucher
  git checkout fonte/backup/stayflow-completo -- apps/frontend/src/pages/BookingStatusPage.jsx apps/frontend/src/pages/MyBookingsPage.jsx
  git add apps/frontend/src/pages/BookingStatusPage.jsx apps/frontend/src/pages/MyBookingsPage.jsx
  git commit -m "feat(frontend): implementa tela de status/voucher e painel de minhas reservas com cancelamento"
  git push -u origin feature/frontend-booking-status-voucher
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/frontend-booking-status-voucher`
  * **Título:** `[Sprint 5] Feat: Telas de Status de Reserva, Voucher e Minhas Reservas`
  * **Reviewer:** Guilherme Neves de Assis

---

#### 📌 Dia 15 | Tarefa 5.2 — Módulo de Avaliações e Notas dos Hotéis
* **Responsável:** **Francisca Bianca da Silva**
* **Revisor Obrigatório:** **Raul de Queiroz Moura**
* **Branch:** `feature/reviews-ratings-api`
* **Arquivos:**
  * `apps/services/core-service/app/models/avaliacao.py`
  * `apps/services/core-service/app/api/v1/avaliacoes.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/reviews-ratings-api
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/models/avaliacao.py apps/services/core-service/app/api/v1/avaliacoes.py
  git add apps/services/core-service/app/models/avaliacao.py apps/services/core-service/app/api/v1/avaliacoes.py
  git commit -m "feat(api): implementa modelo e endpoints de avaliacoes e notas de hoteis"
  git push -u origin feature/reviews-ratings-api
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/reviews-ratings-api`
  * **Título:** `[Sprint 5] Feat: Módulo de Avaliações e Notas de Hotéis`
  * **Reviewer:** Raul de Queiroz Moura

---

### 📊 SPRINT 6 — Painel Administrativo & Orquestração Final

---

#### 📌 Dia 16 | Tarefa 6.1 — Endpoints Administrativos e Registro Geral da API
* **Responsável:** **Raul de Queiroz Moura**
* **Revisor Obrigatório:** **Kelvin Barros Dias**
* **Branch:** `feature/admin-dashboard-backend`
* **Arquivos:**
  * `apps/services/core-service/app/api/v1/admin.py`
  * `apps/services/core-service/app/main.py`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/admin-dashboard-backend
  git checkout fonte/backup/stayflow-completo -- apps/services/core-service/app/api/v1/admin.py apps/services/core-service/app/main.py
  git add apps/services/core-service/app/api/v1/admin.py apps/services/core-service/app/main.py
  git commit -m "feat(admin): implementa endpoints administrativos de gestao e registro geral de rotas"
  git push -u origin feature/admin-dashboard-backend
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/admin-dashboard-backend`
  * **Título:** `[Sprint 6] Feat: Endpoints Administrativos e Registro Geral de Rotas`
  * **Reviewer:** Kelvin Barros Dias

---

#### 📌 Dia 17 | Tarefa 6.2 — Painel Administrativo e Roteamento Geral da Aplicação
* **Responsável:** **Kelvin Barros Dias**
* **Revisor Obrigatório:** **Paula de Freitas Mendes Barbosa**
* **Branch:** `feature/admin-dashboard-frontend`
* **Arquivos:**
  * `apps/frontend/src/pages/admin/AdminDashboard.jsx`
  * `apps/frontend/src/App.jsx`
  * `apps/frontend/src/main.jsx`
  * `apps/frontend/index.html`
* **Passo a passo no terminal:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/admin-dashboard-frontend
  git checkout fonte/backup/stayflow-completo -- apps/frontend/src/pages/admin/AdminDashboard.jsx apps/frontend/src/App.jsx apps/frontend/src/main.jsx apps/frontend/index.html
  git add apps/frontend/src/pages/admin/AdminDashboard.jsx apps/frontend/src/App.jsx apps/frontend/src/main.jsx apps/frontend/index.html
  git commit -m "feat(frontend): implementa painel administrativo integrado e rotas protegidas no app"
  git push -u origin feature/admin-dashboard-frontend
  ```
* **Abertura do PR:**
  * **Base:** `develop` | **Head:** `feature/admin-dashboard-frontend`
  * **Título:** `[Sprint 6] Feat: Painel Administrativo e Roteamento Geral da Aplicação`
  * **Reviewer:** Paula de Freitas Mendes Barbosa

---

## 🎯 Resumo de Entregas por Integrante

| Integrante | Total de PRs Criados | Total de PRs Revisados/Aprovados | Frentes de Atuação |
|---|:---:|:---:|---|
| **Kelvin Barros Dias** | **3** (Dias 4, 11, 17) | **3** (Dias 1, 7, 16) | Auth JWT, Pricing Engine e Admin Frontend |
| **Paula de Freitas Mendes Barbosa** | **4** (Dias 3, 6, 10, 14) | **3** (Dias 4, 11, 17) | Layout Shell, Auth UI, Catálogo UI e Vouchers |
| **Guilherme Neves de Assis** | **3** (Dias 2, 9, 13) | **4** (Dias 3, 6, 10, 14) | DB Config, Catálogo API e Checkout UI |
| **Francisca Bianca da Silva** | **4** (Dias 5, 8, 12, 15) | **3** (Dias 2, 9, 13) | Auth Endpoints, Hotel Models, Reservas API e Avaliações |
| **Raul de Queiroz Moura** | **3** (Dias 1, 7, 16) | **4** (Dias 5, 8, 12, 15) | Docker/Env, Testes Automatizados e Admin Backend |
