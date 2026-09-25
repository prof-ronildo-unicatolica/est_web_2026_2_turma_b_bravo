# 🎯 Roteiro de Apresentação para a Banca Avaliadora

**Projeto:** StayFlow — Sistema de Gestão de Rede Hoteleira  
**Disciplina:** Estágio II em Desenvolvimento Web (2026.2)  
**Turma:** B | **Equipe:** Bravo  
**Data da Apresentação:** _A definir pelo professor_

---

## 📌 Resumo Executivo

O **StayFlow** é um sistema web completo de gestão de rede hoteleira, desenvolvido em 8 sprints pela Equipe Bravo. O projeto implementa uma stack moderna com **FastAPI** (backend), **React + Vite** (frontend), **PostgreSQL** (banco relacional), **MongoDB** (logs de auditoria) e **RabbitMQ** (mensageria assíncrona), tudo orquestrado via **Docker Compose**.

---

## 🗂️ Estrutura da Apresentação (Tempo Estimado: 20min)

### Bloco 1 — Introdução e Contexto (3 min)
1. Apresentação dos integrantes e suas frentes de atuação.
2. Visão geral do problema: necessidade de um sistema centralizado para gestão de múltiplos hotéis.
3. Escopo do MVP: cadastro, busca, reservas com precificação dinâmica, avaliações e painel administrativo.

### Bloco 2 — Arquitetura Técnica (4 min)
1. **Diagrama de Arquitetura**: Frontend SPA ↔ API REST (FastAPI) ↔ PostgreSQL + MongoDB + RabbitMQ.
2. **Autenticação e Segurança**: JWT com hash bcrypt, guards RBAC (`get_current_user`, `get_current_admin`).
3. **Motor de Precificação Dinâmica**: Cálculo de diárias com sazonalidade, tarifas de temporada, early check-in/late checkout e serviços adicionais.
4. **Mensageria Assíncrona**: Publicação de eventos de auditoria no RabbitMQ, consumo pelo `audit_worker` com persistência no MongoDB.

### Bloco 3 — Demonstração ao Vivo (8 min)
1. **Fluxo do Cliente:**
   - Cadastro de novo usuário → Login → Token JWT armazenado.
   - Busca de hotéis por cidade/estrelas → Filtros dinâmicos na HomePage.
   - Seleção de hotel → Detalhes com quartos, comodidades, avaliações e tarifas de temporada.
   - Checkout com simulação de preço em tempo real (seleção de datas, adicionais).
   - Confirmação de reserva → Voucher digital com QR Code.
   - Painel "Minhas Reservas" → Histórico e cancelamento.

2. **Fluxo do Administrador:**
   - Login como admin (`admin@hotel.com` / `admin123`).
   - Dashboard com métricas de ocupação, faturamento e últimas reservas.
   - Aba de logs de auditoria (NoSQL/MongoDB).
   - Gestão de hotéis, quartos e usuários.

3. **API Interativa:**
   - Swagger UI (`/docs`) mostrando todos os endpoints organizados por tags.

### Bloco 4 — Engenharia de Software e Processo (3 min)
1. **Gitflow**: Branches protegidas (`main`, `develop`), nomenclatura Conventional Commits, anel fechado de Code Review.
2. **Sprints e Entregas**: 8 sprints executadas, 24+ Pull Requests mergeados, 7 integrantes com contribuições rastreáveis.
3. **Testes Automatizados**: Suíte Pytest com cobertura de auth (JWT/RBAC), catálogo de hotéis e fluxos de reservas.
4. **Containerização**: `docker compose up -d --build` sobe toda a stack em ambiente isolado.

### Bloco 5 — Conclusão e Perguntas (2 min)
1. Lições aprendidas e desafios técnicos.
2. Possíveis evoluções futuras (gateway de pagamento, notificações push, CI/CD completo).
3. Agradecimentos e abertura para perguntas da banca.

---

## 🖥️ Pré-requisitos para Demonstração

```bash
# Subir toda a stack
docker compose up -d --build

# Executar migrações do banco
docker compose exec backend alembic upgrade head

# Popular dados de demonstração
docker compose exec backend python -m app.db.seed
```

**Portas dos Serviços:**

| Serviço | Porta | URL |
|---------|-------|-----|
| Frontend React | `5173` | http://localhost:5173 |
| Backend FastAPI | `8000` | http://localhost:8000 |
| Swagger / Docs | `8000` | http://localhost:8000/docs |
| PostgreSQL | `5432` | `localhost:5432` |
| MongoDB | `27017` | `localhost:27017` |
| RabbitMQ Management | `15672` | http://localhost:15672 |

---

## 👥 Credenciais de Demonstração

| Perfil | E-mail | Senha |
|--------|--------|-------|
| **Administrador** | `admin@hotel.com` | `admin123` |
| **Cliente Teste** | _(cadastrar na tela de registro)_ | _(livre)_ |

---

## 📊 Métricas do Projeto

| Métrica | Valor |
|---------|-------|
| **Total de Sprints** | 8 |
| **Pull Requests Mergeados** | 24+ |
| **Integrantes Ativos** | 7 |
| **Endpoints da API** | 15+ |
| **Modelos de Domínio (ORM)** | 9 tabelas |
| **Telas do Frontend** | 8 páginas |
| **Cobertura de Testes** | Auth + Domínio Hoteleiro |
