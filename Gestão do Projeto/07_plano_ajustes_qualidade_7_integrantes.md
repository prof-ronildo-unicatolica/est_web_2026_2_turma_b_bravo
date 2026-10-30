# Plano de Ajustes de Qualidade — Divisão para os 7 Integrantes

**Projeto:** Sistema de Gestão Hoteleira — Estágio II (2026.2)  
**Turma:** B | **Equipe:** Bravo (7 Integrantes)  
**Base do Diagnóstico:** Relatório do Professor e Análise SonarQube (`relatorio_qualidade.pdf` e Issues 01 a 05)  
**Status Atual da Equipe:** Rating C  
**Meta Geral:** Subir todos os eixos para **Rating A** (Confiabilidade A, Manutenibilidade A, Complexidade A, Testes A, Segurança A).

---

## 👥 1. Matriz de Distribuição das 7 Frentes de Qualidade

Para que **todos os 7 participantes** contribuam com código e revisão de forma balanceada, as pendências dos 5 relatórios foram distribuídas de acordo com a especialidade técnica de cada membro:

| # | Integrante | Papel Técnico | Issue / Frente Designada | Branch de Trabalho | Revisor do PR |
|---|---|---|---|---|---|
| **P1** | **Guilherme Neves de Assis** | Backend & DB | **Confiabilidade Backend & Refatoração de DB** | `fix/quality-confiabilidade-backend` | Kelvin Barros |
| **P2** | **Kelvin Barros Dias** | Líder Backend / Rotas | **Manutenibilidade: Documentação de HTTPException (Admin & Hotéis)** | `fix/quality-docs-rotas-admin` | Paula de Freitas |
| **P3** | **Paula de Freitas Mendes** | Líder Frontend / UI | **Confiabilidade & Complexidade Frontend (Navbar, Hotel & Admin)** | `fix/quality-frontend-ui-buttons` | Francisca Bianca |
| **P4** | **Francisca Bianca da Silva** | Backend & Domínio | **Manutenibilidade & Complexidade da API de Reservas** | `fix/quality-docs-rotas-reservas` | Raul de Queiroz |
| **P5** | **Raul de Queiroz Moura** | DevOps & QA | **Segurança: Hardening de Containers Docker e Segredos** | `chore/quality-seguranca-docker-env` | Atyla Braga |
| **P6** | **Atyla Braga** | Fullstack & Telas | **Confiabilidade & Refatoração (Checkout & Minhas Reservas)** | `fix/quality-frontend-checkout-bookings` | Herbert Monteiro |
| **P7** | **Herbert Monteiro** | Backend & Avaliações | **Razão de Testes (RNFO07) & Documentação de Avaliações** | `test/quality-services-avaliacoes` | Guilherme Neves |

---

## 🔄 2. Anel Fechado de Code Review (7 Integrantes)

Seguindo o critério avaliativo rigoroso da disciplina:
* Nenhum participante envia código diretamente para a branch `develop`.
* Todo código é submetido por Pull Request (PR) e aprovado pelo colega definido no anel fechado:

```mermaid
graph LR
    P1[Guilherme Neves<br>Backend & DB] -->|PR revisado por| P2[Kelvin Barros<br>Rotas Admin & Hotéis]
    P2 -->|PR revisado por| P3[Paula de Freitas<br>Frontend Shell & UI]
    P3 -->|PR revisado por| P4[Francisca Bianca<br>Rotas Reservas]
    P4 -->|PR revisado por| P5[Raul de Queiroz<br>DevOps & Docker]
    P5 -->|PR revisado por| P6[Atyla Braga<br>Checkout & Bookings]
    P6 -->|PR revisado por| P7[Herbert Monteiro<br>Testes & Avaliações]
    P7 -->|PR revisado por| P1
```

---

## 📋 3. Detalhamento Técnico das Tarefas por Integrante

---

### 🟢 Integrante 1: Guilherme Neves de Assis
* **Frente:** Confiabilidade Backend, Audit Worker e Otimização do DB
* **Metas dos Relatórios:**
  * Eliminar `datetime.utcnow()` em módulos do backend (`01-confiabilidade.pdf`).
  * Repassar exceção de cancelamento (`CancelledError`) no Worker de auditoria (`01-confiabilidade.pdf`).
  * Decompor `db/__init__.py` para reduzir a complexidade cognitiva de 28 para ≤ 15 (`03-complexidade.pdf`).
  * Eliminar repetição de strings literais (`db/__init__.py`).
* **Arquivos Alvo:**
  1. `apps/services/core-service/app/core/security.py`
  2. `apps/services/core-service/app/workers/audit_worker.py`
  3. `apps/services/core-service/app/db/__init__.py`
* **Ações Práticas:**
  1. Em `security.py`: usar `datetime.now(timezone.utc)` e tipagem moderna `str | Any`.
  2. Em `audit_worker.py`: usar `datetime.now(timezone.utc)`, repassar `asyncio.CancelledError` com `raise` após a limpeza e usar `logger.exception()` nos blocos `except`.
  3. Em `db/__init__.py`: extrair constantes para mensagens repetidas e quebrar a inicialização de tabelas e seeds em funções auxiliares dedicadas.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b fix/quality-confiabilidade-backend
  # [realizar alterações nos arquivos]
  git add apps/services/core-service/app/core/security.py apps/services/core-service/app/workers/audit_worker.py apps/services/core-service/app/db/__init__.py
  git commit -m "fix(backend): corrige timezone utc, cancelamento do worker e modulariza init db"
  git push origin fix/quality-confiabilidade-backend
  ```
* **Pull Request:** Destino `develop` | Revisor: **Kelvin Barros**

---

### 🔵 Integrante 2: Kelvin Barros Dias
* **Frente:** Manutenibilidade — Documentação de HTTPException e Refatoração da API Admin
* **Metas dos Relatórios:**
  * Documentar na rota os `HTTPException` que ela lança no Swagger (`02-manutenibilidade.pdf`).
  * Reduzir a complexidade cognitiva da API Admin de 16 para ≤ 10 (`03-complexidade.pdf`).
* **Arquivos Alvo:**
  1. `apps/services/core-service/app/api/v1/admin.py` (linhas 61, 73, 99, 135, 155, 186, 198, 224, 250)
  2. `apps/services/core-service/app/api/v1/hoteis.py` (linha 100)
* **Ações Práticas:**
  1. Adicionar o parâmetro `responses={400: {"description": "Requisição inválida"}, 404: {"description": "Recurso não encontrado"}, 409: {"description": "Conflito"}}` nos decoradores `@router.get`, `@router.post`, `@router.put`, `@router.delete` das rotas administrativas e de hotéis.
  2. Quebrar endpoints com validações longas em `admin.py`, extraindo funções auxiliares de verificação de permissão e sanitização de dados.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b fix/quality-docs-rotas-admin
  # [realizar alterações nos arquivos]
  git add apps/services/core-service/app/api/v1/admin.py apps/services/core-service/app/api/v1/hoteis.py
  git commit -m "fix(api): documenta responses http nos endpoints de admin e hoteis"
  git push origin fix/quality-docs-rotas-admin
  ```
* **Pull Request:** Destino `develop` | Revisora: **Paula de Freitas**

---

### 🟣 Integrante 3: Paula de Freitas Mendes Barbosa
* **Frente:** Confiabilidade & Redução de Complexidade de Componentes Frontend
* **Metas dos Relatórios:**
  * Todo `<button>` deve ter o atributo `type` explícito (`01-confiabilidade.pdf`).
  * Reduzir complexidade dos componentes React `HotelDetailPage.jsx` e `AdminDashboard.jsx` (`03-complexidade.pdf`).
* **Arquivos Alvo:**
  1. `apps/frontend/src/components/layout/Navbar.jsx` (linha 48)
  2. `apps/frontend/src/pages/HotelDetailPage.jsx` (linha 56)
  3. `apps/frontend/src/pages/admin/AdminDashboard.jsx` (linhas 79, 120, 187)
* **Ações Práticas:**
  1. Adicionar `type="button"` no botão de logout da `Navbar.jsx`, nos botões de navegação e filtros da `HotelDetailPage.jsx` e nos botões de ação do `AdminDashboard.jsx`.
  2. Em `AdminDashboard.jsx`: extrair as tabelas de logs e listas de usuários para subcomponentes menores, reduzindo a complexidade do JSX.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b fix/quality-frontend-ui-buttons
  # [realizar alterações nos arquivos]
  git add apps/frontend/src/components/layout/Navbar.jsx apps/frontend/src/pages/HotelDetailPage.jsx apps/frontend/src/pages/admin/AdminDashboard.jsx
  git commit -m "fix(frontend): define type button explicito e modulariza dashboard admin"
  git push origin fix/quality-frontend-ui-buttons
  ```
* **Pull Request:** Destino `develop` | Revisora: **Francisca Bianca**

---

### 🟡 Integrante 4: Francisca Bianca da Silva
* **Frente:** Manutenibilidade & Complexidade da API de Reservas
* **Metas dos Relatórios:**
  * Documentar `HTTPException` lançados em todas as rotas de reservas (`02-manutenibilidade.pdf`).
  * Reduzir a complexidade cognitiva de `reservas.py` de 16 para ≤ 10 (`03-complexidade.pdf`).
* **Arquivos Alvo:**
  1. `apps/services/core-service/app/api/v1/reservas.py` (linhas 47, 60, 76, 152, 154, 168, 170, 172, 174)
* **Ações Práticas:**
  1. Adicionar `responses={400: {"description": "Datas inválidas"}, 404: {"description": "Reserva não encontrada"}, 409: {"description": "Quarto indisponível"}}` nas 9 rotas de reservas.
  2. Substituir `if/else` aninhados por retornos antecipados (*early returns*) nas checagens de disponibilidade e no cálculo de cancelamento.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b fix/quality-docs-rotas-reservas
  # [realizar alterações nos arquivos]
  git add apps/services/core-service/app/api/v1/reservas.py
  git commit -m "fix(api): documenta responses de erro e simplifica logica de reservas"
  git push origin fix/quality-docs-rotas-reservas
  ```
* **Pull Request:** Destino `develop` | Revisor: **Raul de Queiroz**

---

### 🟠 Integrante 5: Raul de Queiroz Moura
* **Frente:** Segurança e Configurações Herdadas (Docker, MongoDB & Variáveis)
* **Metas dos Relatórios:**
  * O Dockerfile não deve copiar o contexto inteiro (`COPY . .`) (`05-seguranca_herdada.pdf`).
  * Senha do MongoDB não deve ficar exposta no código (`05-seguranca_herdada.pdf`).
* **Arquivos Alvo:**
  1. `apps/services/core-service/Dockerfile` (linha 22)
  2. `apps/services/core-service/.dockerignore` (novo)
  3. `apps/services/core-service/app/core/config.py` (linha 23)
  4. `docker-compose.yml` (linhas 69, 100)
  5. `.env.exemplo` (novo ou revisado)
* **Ações Práticas:**
  1. No `Dockerfile`: substituir `COPY . .` por cópias direcionadas (`COPY app ./app`, `COPY alembic ./alembic`, `COPY alembic.ini .`).
  2. Criar `.dockerignore` excluindo `.env`, `.git`, `node_modules`, `__pycache__`, `.pytest_cache`.
  3. Em `config.py`: ler `MONGODB_URL` das variáveis de ambiente via Pydantic Settings, sem senha exposta por padrão.
  4. Em `docker-compose.yml`: usar `${MONGODB_URL:-mongodb://admin:admin123@mongodb:27017}` e documentar no `.env.exemplo`.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/quality-seguranca-docker-env
  # [realizar alterações nos arquivos]
  git add apps/services/core-service/Dockerfile apps/services/core-service/.dockerignore apps/services/core-service/app/core/config.py docker-compose.yml .env.exemplo
  git commit -m "chore(infra): protege contexto docker e isola credenciais do mongodb em env"
  git push origin chore/quality-seguranca-docker-env
  ```
* **Pull Request:** Destino `develop` | Revisor: **Atyla Braga**

---

### 🔵 Integrante 6: Atyla Braga
* **Frente:** Confiabilidade & Refatoração das Telas de Checkout e Minhas Reservas
* **Metas dos Relatórios:**
  * Usar os métodos de `Number` em vez dos globais (`01-confiabilidade.pdf`).
  * Todo `<button>` deve ter `type` explícito (`01-confiabilidade.pdf`).
  * Espaço entre elementos inline deve ser explícito no JSX (`02-manutenibilidade.pdf`).
  * Reduzir complexidade das telas `CheckoutPage.jsx` e `MyBookingsPage.jsx` (`03-complexidade.pdf`).
* **Arquivos Alvo:**
  1. `apps/frontend/src/pages/CheckoutPage.jsx` (linhas 51, 68, 92, 119, 160, 166, 172, 183, 188, 193)
  2. `apps/frontend/src/pages/MyBookingsPage.jsx` (linhas 132, 139, 179, 182)
* **Ações Práticas:**
  1. Trocar `isNaN` por `Number.isNaN`, `parseInt` por `Number.parseInt` e `parseFloat` por `Number.parseFloat`.
  2. Adicionar `type="button"` nos botões de controle e cancelamento de reservas.
  3. Adicionar `{" "}` antes dos links inline no resumo da compra para evitar que texto e links fiquem colados.
  4. Extrair o cálculo de preços, taxas e simulação de cupom para funções utilitárias puras fora do componente.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b fix/quality-frontend-checkout-bookings
  # [realizar alterações nos arquivos]
  git add apps/frontend/src/pages/CheckoutPage.jsx apps/frontend/src/pages/MyBookingsPage.jsx
  git commit -m "fix(frontend): padroniza metodos Number, botoes jsx e espacamento inline"
  git push origin fix/quality-frontend-checkout-bookings
  ```
* **Pull Request:** Destino `develop` | Revisor: **Herbert Monteiro**

---

### 🔴 Integrante 7: Herbert Monteiro
* **Frente:** Razão e Cobertura de Testes (RNFO07) & Documentação de Avaliações
* **Metas dos Relatórios:**
  * Elevar a razão de testes para ≥ 0,24 linhas de teste por linha de produção (`04-razao_teste.pdf`).
  * Cumprir o requisito **RNFO07** (mínimo de 70% de cobertura na camada de Services do backend).
  * Documentar `HTTPException` na API de Avaliações e centralizar strings repetidas (`02-manutenibilidade.pdf`).
* **Arquivos Alvo:**
  1. `apps/services/core-service/app/api/v1/avaliacoes.py` (linhas 31, 33, 35, 39, 44, 49)
  2. `apps/services/core-service/app/models/hotel.py` (linha 25)
  3. `apps/services/core-service/tests/test_pricing_service.py` (novo)
  4. `apps/services/core-service/tests/test_tutorial_service.py` (novo)
* **Ações Práticas:**
  1. Em `avaliacoes.py`: documentar `responses={400: ..., 404: ...}` nas 6 rotas e centralizar strings repetidas.
  2. Criar suíte de testes unitários para o `PricingService`:
     * Teste de cálculo de diárias base.
     * Teste com tarifas sazonais e multiplicadores de alta temporada.
     * Teste de serviços adicionais (café da manhã, estacionamento, pet).
     * Teste de validações e exceções de datas inválidas.
  3. Assegurar que todos os testes passem com 100% de sucesso no `pytest`.
* **Comandos Git:**
  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b test/quality-services-avaliacoes
  # [realizar alterações e criar testes]
  git add apps/services/core-service/app/api/v1/avaliacoes.py apps/services/core-service/app/models/hotel.py apps/services/core-service/tests/
  git commit -m "test(quality): adiciona testes unitarios de pricing service e documenta avaliacoes"
  git push origin test/quality-services-avaliacoes
  ```
* **Pull Request:** Destino `develop` | Revisor: **Guilherme Neves**

---

## 🚀 4. Sequência Recomendada de Merge na Branch `develop`

Para evitar conflitos entre as branches dos 7 integrantes, a mesclagem dos PRs deve seguir esta ordem:

1. 🟡 `chore/quality-seguranca-docker-env` (Raul) — Ajusta infraestrutura e `.dockerignore`.
2. 🟢 `fix/quality-confiabilidade-backend` (Guilherme) — Corrige timezones e modulariza o banco.
3. 🔵 `fix/quality-docs-rotas-admin` (Kelvin) — Documenta rotas administrativas.
4. 🟡 `fix/quality-docs-rotas-reservas` (Bianca) — Documenta rotas de reservas.
5. 🟣 `fix/quality-frontend-ui-buttons` (Paula) — Corrige botões e layout de topo.
6. 🔵 `fix/quality-frontend-checkout-bookings` (Atyla) — Corrige botões e métodos Number nas telas.
7. 🔴 `test/quality-services-avaliacoes` (Herbert) — Valida com testes toda a base integrada.

---

## 🎯 5. Resultado Esperado Após Todos os PRs

Com a integração dessas 7 frentes:
* **Confiabilidade:** Sobe de **E para A** (sem `datetime.utcnow`, botões tipados e `Number.isNaN`).
* **Manutenibilidade:** Sobe de **E para A** (Swagger com todos os status de erro documentados e strings centralizadas).
* **Complexidade:** Sobe de **B para A** (complexidade cognitiva ≤ 44,0 por mil linhas).
* **Testes:** Sobe de **E para A** (cobertura dos Services em conformidade com o RNFO07).
* **Segurança:** Mantém **A** e elimina vazamento de credenciais e arquivos no Docker.
* **Rating Geral:** O repositório sobe de **C para A**, cumprindo 100% das exigências do professor!
