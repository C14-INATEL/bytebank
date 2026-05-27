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

> ℹ️ **GitHub Actions não é utilizado.** O CI/CD é feito via **GitLab CI**.

---

## 🤖 Uso de IA

> *Seção a ser preenchida pelo grupo conforme exigido pela NP2.*

---

## 👥 Equipe

> *Adicionar nomes dos integrantes.*
>
