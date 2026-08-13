# 🚀 Guia de Clonagem do Repositório — Equipe Bravo

Fala equipe! Segue o passo a passo para clonar o repositório oficial da nossa equipe e deixar tudo pronto para começar a trabalhar.

---

## Pré-requisitos

Antes de começar, certifiquem-se de ter instalado:
- **Git** → [Download aqui](https://git-scm.com/downloads)
- **Docker Desktop** → [Download aqui](https://www.docker.com/products/docker-desktop/)
- Uma conta no **GitHub** com acesso ao repositório da equipe

---

## Passo a Passo

### 1️⃣ Abra o terminal

- **Windows**: Abra o **Git Bash** (vem junto com o Git) ou o **Prompt de Comando**
- **Mac**: Abra o **Terminal**
- **Linux**: Abra o **Terminal**

### 2️⃣ Navegue até a pasta onde deseja salvar o projeto

Escolha uma pasta de sua preferência. Exemplo:

```bash
cd ~/Desktop
```

> 💡 Pode ser qualquer pasta, como `Documentos`, `Projetos`, etc.

### 3️⃣ Clone o repositório da equipe

```bash
git clone https://github.com/prof-ronildo-unicatolica/est_web_2026_2_turma_b_bravo.git
```

Isso vai criar uma pasta chamada `est_web_2026_2_turma_b_bravo` com todo o código do projeto.

### 4️⃣ Entre na pasta do projeto

```bash
cd est_web_2026_2_turma_b_bravo
```

### 5️⃣ Verifique em qual branch você está

```bash
git branch
```

Você deve ver algo como:

```
* develop
```

> ✅ A branch padrão do repositório já é a **`develop`**, que é a nossa branch de trabalho. Se por acaso aparecer `main`, rode: `git checkout develop`

### 6️⃣ Copie o arquivo de variáveis de ambiente

```bash
cp .env.example .env
```

> Esse arquivo contém as credenciais do banco de dados e outras configurações locais. Ele **não vai pro GitHub** (está no `.gitignore`).

### 7️⃣ Suba toda a stack com Docker

```bash
docker compose up -d --build
```

> ⏳ Na primeira vez demora alguns minutos para baixar as imagens e construir os containers. Tenham paciência!

### 8️⃣ Verifique se tudo está rodando

```bash
docker compose ps
```

Todos os serviços devem estar com status **"Up"** ou **"running"**.

### 9️⃣ Teste os acessos

Abram no navegador:

| Serviço | URL |
|---|---|
| **Frontend (React)** | http://localhost:5173 |
| **API + Swagger** | http://localhost:8000/docs |
| **Painel do RabbitMQ** | http://localhost:15672 |

> Se a página do Swagger (`/docs`) abrir com a listagem das rotas, está tudo certo! ✅

---

## ⚠️ Regras Importantes (leiam com atenção!)

1. **Nunca façam commit direto na `develop` ou na `main`.**
2. Sempre criem uma **branch nova** a partir da `develop` para trabalhar:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/nome-da-sua-tarefa
   ```
3. Quando terminar, façam **push da sua branch** e abram um **Pull Request** no GitHub com destino à `develop`:
   ```bash
   git add .
   git commit -m "feat(modulo): descricao do que foi feito"
   git push -u origin feature/nome-da-sua-tarefa
   ```
4. O PR precisa de **pelo menos 1 aprovação** de um colega antes do merge.

---

## 🆘 Problemas comuns

**"Permissão negada" ao clonar:**
- Verifique se você foi adicionado como colaborador no repositório. Se não foi, me avisem que resolvo.

**Docker não sobe:**
- Certifiquem-se de que o **Docker Desktop** está aberto e rodando antes de executar o `docker compose up`.

**Porta já em uso:**
- Se alguma porta (5173, 8000, etc.) já estiver ocupada, fechem o programa que está usando ou alterem no `.env`.

---

Qualquer dúvida, mandem no grupo! 💪
