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

O grupo não adotou formalmente nenhuma metodologia ágil estruturada. Na prática, o desenvolvimento aconteceu de forma colaborativa e informal, com características que se aproximam do **Kanban** — o mais próximo que chegamos de uma metodologia definida.

O trabalho foi organizado por funcionalidades: cada membro ficou responsável por uma área do sistema e o progresso era acompanhado nas reuniões semanais pelo Discord. Não houve sprints formais, quadro Kanban explícito, nem cerimônias definidas — as decisões foram tomadas de forma direta entre os integrantes conforme a necessidade.

---

### Papéis no grupo

| Papel | Responsável | Atribuições principais |
|-------|-------------|------------------------|
| Backend — modelos e rotas | Henrique Fonseca e Felipe Fonseca | Arquitetura Flask, serviços, modelos e autenticação JWT |
| Frontend | Luis Otávio Amante | Componentes React, integração com a API, telas de login e dashboard |
| Testes e pipeline | Felipe Fonseca, Henrique Fonseca e Luis Otávio Amante | Testes unitários (pytest e vitest) e configuração do GitLab CI |

---

### Ferramentas utilizadas

- **Comunicação:** Discord — chamadas de voz semanais e canal de texto para decisões rápidas
- **Versionamento:** GitLab com branches por funcionalidade e pull requests para mergear na `main`
- **Período de desenvolvimento:** Março a Junho de 2026

---


## 🔁 Dinâmica de Desenvolvimento

### Como o trabalho aconteceu na prática

O desenvolvimento foi dividido em duas frentes paralelas desde o início: **backend** (Flask + MongoDB) e **frontend** (React + Vite). Essa separação evitou conflitos frequentes de código e permitiu que cada dupla avançasse de forma independente, integrando via API REST.

As decisões técnicas foram tomadas coletivamente nas reuniões semanais do Discord. Quando surgiam dúvidas ou bloqueios no meio da semana, o canal de texto servia para resolver rapidamente sem precisar esperar a próxima reunião.

---

### Divisão de tarefas

| Área | Integrante(s) | Principais entregas |
|------|------------|---------------------|
| Backend — modelos e banco | `[Henrique]` | `models.py`, conexão MongoDB, estrutura de dados |
| Backend — serviços e regras de negócio | `[Felipe]` | `services.py`, validações, lógica de transações e dashboard |
| Backend — rotas e autenticação | `[Henrique]` | `routes.py`, middleware JWT, endpoints REST |
| Frontend — telas e componentes | `[Luis Otávio]` | `Login.jsx`, `Cadastro.jsx`, `Dashboard.jsx` |
| Testes unitários | `[Felipe, Henrique e Luis Otávio]` | `test_funcoes.py`, testes vitest |
| Pipeline CI/CD | `[Felipe, Henrique e Luis Otávio]` | `.gitlab-ci.yml`, stages e jobs |

---

### Fluxo de branches e padrão de commits

O grupo adotou o seguinte fluxo de branches:

- `main` — branch principal, sempre estável e com pipeline passando
- `feature/[nome-da-funcionalidade]` — criada para cada nova funcionalidade (ex: `feature/autenticacao-jwt`, `feature/crud-transacoes`)
- `fix/[descricao]` — para correções de bugs identificados

**Padrão de commits** adotado:

| Prefixo | Uso |
|---------|-----|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `test:` | Adição ou ajuste de testes |
| `docs:` | Alterações em documentação |
| `ci:` | Mudanças no pipeline |
| `refactor:` | Refatoração sem mudança de comportamento |

**Processo de code review:** todo merge para a `main` era feito via pull request, com revisão obrigatória de ao menos um outro membro antes do merge.

---

### O que funcionou bem

- A separação backend/frontend desde o início eliminou a maioria dos conflitos de merge
- O uso de issues no GitLab manteve as tarefas visíveis para todos
- Os testes unitários do backend (pytest) ajudaram a identificar bugs de lógica antes da integração
- O pipeline automatizado deu confiança para mergear sem quebrar o projeto

---

### O que travou

- **Integração frontend ↔ backend:** os primeiros testes de integração falharam por problemas de CORS e diferenças no formato de resposta da API — resolvido adicionando `flask-cors` e padronizando os campos retornados
- **Configuração do MongoDB Atlas:** a criação do cluster e a liberação de IPs levou mais tempo do que esperado no início do projeto

---

### Lições aprendidas

- **Usar variáveis de ambiente desde o primeiro commit** — hardcodar credenciais no código gerou retrabalho e um risco de segurança real que precisou ser corrigido
- **Escrever testes junto com o código**, não depois — as funcionalidades testadas desde cedo tiveram menos regressões durante a integração
- **Commits menores e mais frequentes** facilitam o code review e tornam o histórico mais legível
- **Documentar decisões técnicas** (mesmo que brevemente na issue) ajuda quando outro membro precisa entender o contexto semanas depois

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

O uso de Inteligência Artificial foi adotado de forma transparente ao longo do projeto, como ferramenta de apoio ao desenvolvimento — e não como substituto do entendimento técnico do grupo.

---

### Modelos utilizados

| Modelo | Plataforma | Uso principal |
|--------|-----------|---------------|
| Claude Sonnet (Anthropic) | claude.ai | Geração de código, debugging, documentação, refatoração, pipeline CI/CD |

---

### Para quê foi usado

- **Geração de código:** estrutura inicial do `Dashboard.jsx`, integração com a API REST, pipeline GitLab CI completo com 6 stages
- **Refatoração:** migração do Dashboard de `localStorage` para consumo real da API; remoção de credenciais hardcoded do `__init__.py` para variáveis de ambiente
- **Debugging:** identificação da causa do erro `ReferenceError: API is not defined` e do erro de conexão ao adicionar transações
- **Documentação:** geração das histórias de usuário (US-01 a US-06), seções de Metodologia e Dinâmica de Desenvolvimento do README
- **CI/CD:** criação do `.gitlab-ci.yml` com stages de install, test, build, package, deploy e notify

---

### Exemplos reais de prompts utilizados

**Prompt 1 — Integração com a API (aceito com ajustes)**
> *"Verifique todas as funcionalidades e os botões que estão faltando, o dinheiro inicial está com um bug e não está começando com 0"*

A IA identificou 8 problemas no Dashboard (uso de localStorage em vez da API, busca não funcional, botões sem ação, valor 0 bloqueado, campo categoria ausente) e reescreveu o componente incompleto.

---

**Prompt 2 — Pipeline CI/CD (aceito com ajuste de branch)**
> *"Crie um pipeline base que contenha isso: instalação de dependências; execução de testes; validação/build do projeto; empacotamento ou geração de artefatos; simulação de deploy; notificações ou mensagens de status da pipeline."*

A IA gerou o `.gitlab-ci.yml` com 6 stages e 10 jobs. O grupo ajustou o job `deploy-simulation` para apontar para a branch correta do repositório (`main`) e confirmou que nenhum job usa GitHub Actions (requisito da disciplina).

---

**Prompt 3 — Refatoração de segurança (aceito integralmente)**
> *"Ajuste o `__init__.py` — as credenciais do MongoDB não é recomendada estarem hardcoded no código"*

A IA migrou as credenciais para variáveis de ambiente usando `python-dotenv`, criou o `.env.example` e explicou que a `SECRET_KEY` é usada para assinar tokens JWT. O grupo entendeu a mudança, atualizou o `.env` local e confirmou que o `.env` já estava no `.gitignore`.

---

### Dinâmica de uso

- A IA foi usada **individualmente** por cada membro conforme a necessidade da sua tarefa
- Nenhum código gerado foi commitado sem revisão — todo output foi lido, testado e entendido antes de ser incorporado
- Em alguns casos a resposta foi **ajustada** (ex: números de issue nas histórias de usuário foram trocados pelos reais do GitLab)
- Em outros casos foi **descartada** parcialmente (ex: sugestão de usar `localStorage` foi descartada em favor da integração real com a API)

---

### O que **não** foi feito por IA

- Lógica de negócio do backend (`services.py`) — desenvolvida manualmente pelo grupo
- Modelagem do banco de dados MongoDB — decisão de estrutura tomada pelo grupo
- Decisões de arquitetura (separação backend/frontend, escolha do MongoDB, uso do GitLab CI) — tomadas pelo grupo
- Ajustes no pipeline conforme o andamento do projeto

---

## 👥 Equipe

| Nome | GitHub               |
|------|----------------------|
| Felipe Fonseca | `[@FelpsFonseca]`    |
| Henrique Fonseca | `[@Hfc10]`           |
| Luis Otávio Amante | `[@luizotavio-amante]` |
