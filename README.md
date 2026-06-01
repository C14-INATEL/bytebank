# 💰 ByteBank

<p align="center">
  Sistema de controle de finanças pessoais para gerenciamento de receitas e despesas.
</p>

<p align="center">
  🚧 Projeto acadêmico em desenvolvimento — INATEL C14 Engenharia de Software
</p>

---

## 📌 Sobre o Projeto

O **ByteBank** é uma aplicação web que auxilia usuários no controle de suas finanças pessoais, permitindo o registro, organização e análise de receitas e despesas. O sistema oferece dashboard com resumo financeiro, gráficos por categoria e histórico completo de transações.

---

## 🚀 Funcionalidades

- 🔐 Cadastro de usuários
- 🔑 Login com autenticação JWT
- 💸 Registro de receitas e despesas
- ✏️ Edição e exclusão de transações
- 📊 Dashboard com resumo financeiro (saldo, receitas, despesas)
- 📈 Gráficos de gastos por categoria
- 🧾 Histórico de transações

---

## 🏗️ Arquitetura

- Arquitetura em **3 camadas** (Apresentação → Serviço → Dados)
- Backend estruturado no padrão **MVC**
- Comunicação via **API REST** com autenticação **JWT**
- Banco de dados **MongoDB Atlas** (cloud)

---

## 📂 Estrutura do Projeto

```
ByteBank/
├── Backend/
│   └── app/
│       ├── __init__.py       # configuração Flask + conexão MongoDB
│       ├── models.py         # modelos de dados (User, Transaction)
│       ├── routes.py         # endpoints da API REST
│       ├── services.py       # regras de negócio
│       └── testes/
│           └── test_funcoes.py  # testes unitários (pytest)
├── Frontend/
│   ├── src/
│   │   ├── App.jsx           # roteamento principal
│   │   ├── Login.jsx         # tela de login
│   │   ├── Cadastro.jsx      # tela de cadastro
│   │   ├── Dashboard.jsx     # painel financeiro
│   │   └── Tests/
│   │       ├── App.test.jsx      # testes de navegação
│   │       ├── dashboard.test.jsx
│   │       └── mock.test.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitlab-ci.yml            # pipeline CI/CD (GitLab CI)
├── requirements.txt          # dependências Python
├── run.py                    # ponto de entrada do backend
└── README.md
```

---

## 📖 Histórias de Usuário

### US-01 — Autenticação segura com JWT

> Como **usuário cadastrado**, eu quero fazer login com email e senha para que meus dados financeiros sejam acessados apenas por mim.

| Campo       | Valor                          |
|-------------|--------------------------------|
| Prioridade  | Alta                           |
| Status      | Entregue                       |

**Critérios de aceitação**

**Cenário 1 — Login com credenciais válidas**
- **Given** que o usuário está na tela de login com email e senha preenchidos corretamente
- **When** ele clica em "Entrar"
- **Then** o sistema autentica via `POST /api/login`, retorna um token JWT válido e redireciona para o Dashboard

**Cenário 2 — Login com credenciais inválidas**
- **Given** que o usuário informa email inexistente ou senha errada
- **When** ele tenta fazer login
- **Then** a API retorna HTTP 401 e a interface exibe uma mensagem de erro sem expor detalhes internos

**Cenário 3 — Acesso a rota protegida sem token**
- **Given** que o usuário tenta acessar qualquer rota protegida sem o header `Authorization: Bearer <token>`
- **When** a requisição chega ao backend
- **Then** o middleware JWT bloqueia e retorna HTTP 401

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #3 — Implementar autenticação JWT | `routes.py → token_required` | `TestRotaLogin`, `TestMiddlewareJWT` |

---

### US-02 — Registro de receitas e despesas

> Como **usuário autenticado**, eu quero registrar uma transação financeira (receita ou despesa) com categoria, valor e descrição para que eu possa controlar meu fluxo de caixa.

| Campo       | Valor                          |
|-------------|--------------------------------|
| Prioridade  | Alta                           |
| Status      | Entregue                       |

**Critérios de aceitação**

**Cenário 1 — Registro de transação válida**
- **Given** que o usuário está no Dashboard e preenche tipo, categoria, valor positivo e descrição
- **When** ele clica em "Adicionar"
- **Then** a transação é salva via `POST /api/transactions`, vinculada ao seu `user_id`, e aparece imediatamente no histórico

**Cenário 2 — Registro com valor inválido**
- **Given** que o usuário tenta registrar uma transação com valor zero ou negativo
- **When** o backend recebe os dados
- **Then** a API retorna HTTP 422 com a mensagem "O valor deve ser um número positivo."

**Cenário 3 — Edição de transação existente**
- **Given** que o usuário deseja editar uma transação já registrada
- **When** ele envia `PUT /api/transactions/:id` com os campos a alterar
- **Then** apenas os campos enviados são atualizados e o sistema retorna o documento atualizado com HTTP 200

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #7 — CRUD de transações | `services.py → TransactionService` | `TestTransactionService`, `TestRotaTransacoes` |

---

## 🛠️ Tecnologias Utilizadas

### 🎨 Frontend

- React 19 + Vite
- JavaScript (ES Modules)
- Vitest + Testing Library (testes)

### ⚙️ Backend

- Python 3.11 + Flask
- PyJWT (autenticação)
- pytest (testes)

### 🗄️ Banco de Dados

- MongoDB Atlas (pymongo)

### 🔧 Ferramentas

- Git + GitHub (versionamento)
- GitLab CI (pipeline CI/CD)
- npm (Frontend) + pip (Backend) — gerenciamento de dependências

---

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- Acesso à internet (MongoDB Atlas)

### Backend

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd ByteBank

# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor
python run.py
```

O backend sobe em `http://localhost:5000`.

### Frontend

```bash
cd Frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend sobe em `http://localhost:5173`.

---

## 🧪 Testes

### Backend (pytest)

```bash
cd Backend
python -m pytest app/testes/test_funcoes.py -v
```

### Frontend (vitest)

```bash
cd Frontend
npm test
```

---

## 🔌 Endpoints da API

Todos os endpoints abaixo exigem o header `Authorization: Bearer <token>`, exceto `/api/users` e `/api/login`.

| Método    | Endpoint                  | Descrição                   |
| ---------- | ------------------------- | ----------------------------- |
| `POST`   | `/api/users`            | Cadastro de novo usuário     |
| `POST`   | `/api/login`            | Login — retorna token JWT    |
| `GET`    | `/api/dashboard`        | Resumo financeiro do usuário |
| `GET`    | `/api/transactions`     | Lista todas as transações   |
| `POST`   | `/api/transactions`     | Cria nova transação         |
| `PUT`    | `/api/transactions/:id` | Edita uma transação         |
| `DELETE` | `/api/transactions/:id` | Remove uma transação        |

---

## 🔄 Pipeline CI/CD (GitLab CI)

O arquivo `.gitlab-ci.yml` na raiz define o pipeline com dois jobs executados automaticamente a cada push:

| Job                | Imagem               | O que faz                               |
| ------------------ | -------------------- | --------------------------------------- |
| `backend-tests`  | `python:3.11-slim` | Instala dependências e roda `pytest` |
| `frontend-tests` | `node:20-slim`     | Instala dependências e roda `vitest` |

---

## 🤖 Uso de IA

> preencher

---

## 👥 Equipe

> nomes
>
