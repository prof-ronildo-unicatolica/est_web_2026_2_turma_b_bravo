# Padronização de Nomenclaturas e Fluxo de Trabalho (Git & Código)

**Projeto:** Sistema de Gestão Hoteleira — Estágio II (2026.2)  
**Equipe:** Bravo (Turma B)  
**Gestor do Projeto:** AI Project Manager  

---

## 1. Fluxo de Git (Gitflow Adaptado)

Para garantir a estabilidade do código e facilitar a integração contínua, adotaremos as seguintes regras rigorosas de versionamento:

* **Branch Principal (`main`)**: Código estável e pronto para produção/entregas finais. **Push direto é proibido**.
* **Branch de Desenvolvimento (`develop`)**: Código em integração da Sprint corrente. **Push direto é proibido**.
* **Branches de Funcionalidade (`feature/*`)**: Criadas a partir de `develop` para desenvolver novas tarefas.
* **Branches de Correção (`fix/*`)**: Criadas para corrigir bugs encontrados em `develop`.

---

## 2. Nomenclatura de Branches

Toda nova branch deve seguir o padrão minúsculo com separadores por hífen (`-`):

* `feature/<modulo>-<descricao-curta>`
  * *Exemplo:* `feature/auth-jwt-backend`
  * *Exemplo:* `feature/login-screen-frontend`
* `fix/<modulo>-<descricao-bug>`
  * *Exemplo:* `fix/cors-header-error`
* `chore/<tarefa-infra>`
  * *Exemplo:* `chore/docker-env-config`

---

## 3. Padrão de Commits (Conventional Commits)

Os commits devem ser claros e objetivos, utilizando os prefixos padronizados em português ou inglês:

* `feat:` Adição de nova funcionalidade.
  * *Exemplo:* `feat(auth): adiciona geracao de token JWT no login`
* `fix:` Correção de um erro/bug.
  * *Exemplo:* `fix(deps): corrige erro de importacao no deps.py`
* `docs:` Alterações na documentação.
  * *Exemplo:* `docs(readme): atualiza instrucoes do docker`
* `style:` Ajustes de formatação sem alterar lógica (espaços, linter).
  * *Exemplo:* `style(frontend): ajusta alinhamento dos botoes na navbar`
* `refactor:` Reformulação de código sem alterar comportamento externo.
  * *Exemplo:* `refactor(services): melhora estrutura do auth_service`
* `test:` Adição ou correção de testes automatizados.
  * *Exemplo:* `test(auth): adiciona testes de integracao para rota /auth/register`

---

## 4. Regras de Pull Requests (PR) e Code Review

1. **Destino Obrigatório**: Todo PR deve ter como destino a branch `develop`.
2. **Título do PR**: Deve seguir a nomenclatura `[Sprint X] Tipo: Descrição resumida`.
   * *Exemplo:* `[Sprint 2] Feat: Implementação do módulo de autenticação JWT`
3. **Descrição Mínima do PR**:
   - O que foi feito?
   - Como testar localmente?
   - Checklist de Definition of Done (DoD) preenchido.
4. **Revisores**: Todo PR necessita de **pelo menos 1 aprovação** de um colega da Equipe Bravo antes de ser mesclado (*merged*). O autor do PR **não pode aprovar** seu próprio PR.
