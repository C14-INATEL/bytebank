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

### US-03 — Dashboard financeiro com resumo e categorias

> Como **usuário autenticado**, eu quero visualizar meu saldo atual, total de receitas, total de despesas e gastos por categoria para que eu entenda rapidamente minha situação financeira.

| Campo       | Valor                          |
|-------------|--------------------------------|
| Prioridade  | Alta                           |
| Status      | Entregue                       |

**Critérios de aceitação**

**Cenário 1 — Visualização do resumo financeiro**
- **Given** que o usuário está autenticado e possui transações registradas
- **When** ele acessa `GET /api/dashboard`
- **Then** a resposta contém `total_receitas`, `total_despesas`, `saldo` e `gastos_por_categoria` calculados corretamente

**Cenário 2 — Dashboard sem transações**
- **Given** que o usuário não possui nenhuma transação cadastrada
- **When** ele acessa o dashboard
- **Then** todos os totais retornam zero e `gastos_por_categoria` retorna objeto vazio, sem erros

**Cenário 3 — Isolamento de dados entre usuários**
- **Given** que dois usuários diferentes estão autenticados simultaneamente
- **When** cada um acessa seu dashboard
- **Then** cada resposta exibe apenas as transações vinculadas ao `user_id` do próprio token, sem vazamento de dados entre contas

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #11 — Endpoint de dashboard | `services.py → get_dashboard` | `TestRotaDashboard` |

---
### US-04 — Cadastro de novo usuário

> Como **visitante**, eu quero criar uma conta com nome, email e senha para que eu possa acessar o ByteBank e começar a gerenciar minhas finanças.

| Campo       | Valor                          |
|-------------|--------------------------------|
| Prioridade  | Alta                           |
| Status      | Entregue                       |

**Critérios de aceitação**

**Cenário 1 — Cadastro com dados válidos**
- **Given** que o visitante preenche nome, email válido e senha na tela de cadastro
- **When** ele confirma o cadastro via `POST /api/users`
- **Then** o sistema cria a conta, armazena a senha como hash (nunca em texto puro) e retorna HTTP 201 com os dados do usuário criado

**Cenário 2 — Email já cadastrado**
- **Given** que já existe uma conta com o email informado
- **When** outro visitante tenta se cadastrar com o mesmo email
- **Then** a API retorna HTTP 409 com mensagem de email já cadastrado, sem criar duplicata

**Cenário 3 — Campos obrigatórios ausentes**
- **Given** que o visitante envia o formulário sem preencher todos os campos obrigatórios
- **When** o backend recebe a requisição incompleta
- **Then** a API retorna HTTP 400 indicando os campos faltantes, sem criar nenhum registro

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #2 — Cadastro de usuário | `services.py → criar_usuario` / `routes.py → POST /api/users` | `TestUserModel`, `TestUserService`, `TestRotaUsuarios` |

---

### US-05 — Exclusão de transação

> Como **usuário autenticado**, eu quero excluir uma transação registrada por engano para que meu histórico financeiro reflita apenas lançamentos corretos.

| Campo       | Valor                          |
|-------------|--------------------------------|
| Prioridade  | Média                          |
| Status      | Entregue                       |

**Critérios de aceitação**

**Cenário 1 — Exclusão de transação existente**
- **Given** que o usuário autenticado possui uma transação existente com `id` conhecido
- **When** ele envia `DELETE /api/transactions/:id` com token válido
- **Then** a transação é removida do banco, a API retorna HTTP 200 e o item desaparece do histórico

**Cenário 2 — Exclusão de transação inexistente**
- **Given** que o usuário tenta excluir uma transação com `id` inexistente ou já deletado
- **When** o backend processa o `DELETE`
- **Then** a API retorna HTTP 404 com mensagem "Transação não encontrada", sem lançar exceção

**Cenário 3 — Exclusão de transação de outro usuário**
- **Given** que um usuário autenticado tenta excluir uma transação que pertence a outro usuário
- **When** o backend valida o `user_id` do token contra o dono do registro
- **Then** a API retorna HTTP 403 e a transação permanece intacta no banco

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #8 — Exclusão de transação | `services.py → deletar_transacao` / `routes.py → DELETE /api/transactions/:id` | `TestTransactionService` → `test_deletar_transacao_existente`, `test_deletar_transacao_inexistente` |

---

### US-06 — Histórico de transações

> Como **usuário autenticado**, eu quero visualizar a lista completa das minhas transações para que eu possa acompanhar todos os meus lançamentos financeiros em um só lugar.

| Campo       | Valor      |
|-------------|------------|
| Prioridade  | Média      |
| Status      | Entregue   |

**Critérios de aceitação**

**Cenário 1 — Listagem com transações existentes**
- **Given** que o usuário está autenticado e possui transações registradas
- **When** ele acessa `GET /api/transactions` com token válido
- **Then** a API retorna HTTP 200 com a lista de todas as suas transações, incluindo tipo, categoria, valor, descrição e data de cada registro

**Cenário 2 — Listagem sem transações**
- **Given** que o usuário não possui nenhuma transação cadastrada
- **When** ele acessa o histórico
- **Then** a API retorna HTTP 200 com uma lista vazia, sem erros

**Cenário 3 — Isolamento entre usuários**
- **Given** que dois usuários distintos possuem transações cadastradas
- **When** cada um lista seu histórico
- **Then** cada resposta contém apenas as transações vinculadas ao `user_id` do próprio token, garantindo isolamento total entre contas

**Rastreabilidade**

| Issue / PR | Código | Testes automatizados |
|------------|--------|----------------------|
| #9 — Listagem de transações | `services.py → listar_transacoes` / `routes.py → GET /api/transactions` | `TestTransactionService` → `test_listar_transacoes_retorna_lista`, `test_listar_transacoes_usuario_sem_transacoes`, `test_listar_transacoes_ids_sao_strings` |

---

## 🗂️ Metodologia de Desenvolvimento

### Metodologia adotada — Kanban com cadência semanal

O grupo adotou uma abordagem *Kanban* adaptada ao contexto acadêmico, combinada com elementos de revisão de código inspirados em práticas do *XP (Extreme Programming)*. A escolha pelo Kanban se deu pela flexibilidade de não exigir sprints rígidos, sendo mais compatível com a rotina de estudantes com cargas horárias variáveis entre as semanas.

Em vez de sprints formais, o grupo operou em *ciclos semanais informais*: a cada semana as issues abertas eram priorizadas e distribuídas, e ao final da semana o andamento era revisado via Discord.

---

### Papéis no grupo

| Papel | Responsável | Atribuições principais |
|-------|-------------|------------------------|
| Product Owner (PO) | [Henrique, Luis Otavio e Felipe] | Definição de prioridades, escopo das funcionalidades e histórias de usuário |
| Tech Lead / Backend | [Henrique e Felipe] | Arquitetura Flask, serviços, modelos e autenticação JWT |
| Desenvolvedor Frontend | [Luis Otavio] | Componentes React, integração com a API, telas de login e dashboard |
| QA / Testes | [Henrique, Luis Otavio e Felipe] | Escrita e manutenção dos testes unitários (pytest e vitest) |
| DevOps / CI-CD | [Henrique e Luis Otavio] | Configuração e manutenção do pipeline GitLab CI |


---

### Cadência e ferramentas

- *Reuniões:* encontros semanais por chamada de voz no *Discord* ([Quarta e Sexta], aproximadamente [13:30])
- *Comunicação assíncrona:* canal de texto no Discord para dúvidas, decisões rápidas e compartilhamento de links
- *Gerenciamento de tarefas:* issues do *GitLab* como quadro Kanban (colunas: Open → In Progress → Closed)
- *Versionamento:* GitLab com fluxo de branches por funcionalidade e pull requests obrigatórios para mergear na main
- *Período de desenvolvimento:* [Março] a [Junho] de [2026]

---

### Definição de Pronto (DoD) e Definição de Preparado (DoR)

*Definição de Preparado (DoR)* — uma issue só era iniciada quando:
- O escopo estava claro e descrito na issue
- Não havia dependência bloqueante de outra tarefa em aberto

*Definição de Pronto (DoD)* — uma tarefa só era considerada concluída quando:
- O código estava implementado e funcionando localmente
- Ao menos um teste unitário relevante cobria a funcionalidade
- O pull request havia sido revisado e aprovado por ao menos um outro membro
- O pipeline passava sem erros após o merge

---

### Métricas do projeto

| Métrica | Valor |
|---------|-------|
| Total de issues abertas | [Nº] |
| Total de issues fechadas | [Nº] |
| Total de pull requests mergeados | [Nº] |
| Média de issues fechadas por ciclo semanal | [Nº] |
| Cobertura de testes (backend) | [XX%] |


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

O arquivo `.gitlab-ci.yml` define o pipeline com **6 stages** e **10 jobs** executados automaticamente a cada push:

| Stage | Job | O que faz |
|-------|-----|-----------|
| `install` | `install-backend` | Instala dependências Python via pip |
| `install` | `install-frontend` | Instala dependências Node via npm ci |
| `test` | `backend-tests` | Roda pytest com cobertura e exporta relatório JUnit |
| `test` | `frontend-lint` | Valida código com ESLint |
| `test` | `frontend-tests` | Roda vitest e exporta relatório JUnit |
| `build` | `frontend-build` | Gera build de produção com Vite |
| `build` | `backend-validate` | Valida inicialização do Flask |
| `package` | `package-backend` | Empacota backend em `.tar.gz` com hash do commit |
| `package` | `package-frontend` | Empacota frontend (dist) em `.tar.gz` |
| `deploy` | `deploy-simulation` | Simula deploy completo (apenas na branch `main`) |
| `notify` | `notify-success` | Exibe resumo de sucesso ao fim do pipeline |
| `notify` | `notify-failure` | Exibe diagnóstico de falha quando algum job falha |

---

## 🤖 Uso de IA

> preencher

---

## 👥 Equipe

> nomes
>
