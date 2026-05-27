"""
Testes unitários do ByteBank Backend
Cobertura: models, services, routes (via Flask test client)
"""
import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# ── Importações dos módulos testados ──────────────────────────────────────────
from app.models import User, Transaction
from app.services import UserService, TransactionService


# ══════════════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_db():
    """Mock do objeto db do MongoDB (substitui o MongoClient real)."""
    db = MagicMock()
    # Por padrão find_one retorna None (sem duplicatas de email)
    db.users.find_one.return_value = None
    return db


@pytest.fixture
def app():
    """Flask test app com MongoClient mockado."""
    with patch("pymongo.MongoClient"):
        from app import create_app
        application = create_app()
        application.config["TESTING"] = True
        application.config["SECRET_KEY"] = "chave_de_teste"
        yield application


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def valid_token(app):
    """JWT válido para testes de rotas protegidas."""
    with app.app_context():
        return jwt.encode(
            {"user_id": "user123", "exp": datetime.utcnow() + timedelta(hours=2)},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )


@pytest.fixture
def auth_headers(valid_token):
    """Header Authorization com token válido."""
    return {"Authorization": f"Bearer {valid_token}"}


# ══════════════════════════════════════════════════════════════════════════════
# TESTES DE MODELS
# ══════════════════════════════════════════════════════════════════════════════

class TestUserModel:
    def test_criacao_usuario_campos_corretos(self):
        """User armazena username e email corretamente."""
        u = User(username="ana", email="ana@bytebank.com", password="senha123")
        assert u.username == "ana"
        assert u.email == "ana@bytebank.com"

    def test_senha_armazenada_como_hash(self):
        """A senha nunca deve ser armazenada em texto puro."""
        u = User(username="ana", email="ana@bytebank.com", password="senha123")
        assert u.password_hash != "senha123"
        assert len(u.password_hash) > 10

    def test_check_password_correto(self):
        """check_password retorna True para a senha certa."""
        u = User(username="ana", email="ana@bytebank.com", password="senha123")
        assert u.check_password("senha123") is True

    def test_check_password_errado(self):
        """check_password retorna False para senha errada."""
        u = User(username="ana", email="ana@bytebank.com", password="senha123")
        assert u.check_password("errada") is False

    def test_id_inicializa_como_none(self):
        """id deve ser None antes de ser persistido no banco."""
        u = User(username="x", email="x@x.com", password="abc")
        assert u.id is None

    def test_dois_usuarios_hashes_diferentes(self):
        """Mesma senha em usuários distintos gera hashes diferentes (salt)."""
        u1 = User(username="a", email="a@a.com", password="igual")
        u2 = User(username="b", email="b@b.com", password="igual")
        assert u1.password_hash != u2.password_hash


class TestTransactionModel:
    def test_criacao_receita_valida(self):
        """Transaction de tipo 'receita' é criada sem erros."""
        t = Transaction(user_id=1, type="receita",
                        category="salario", amount=3000.0)
        assert t.type == "receita"
        assert t.amount == 3000.0

    def test_criacao_despesa_valida(self):
        """Transaction de tipo 'despesa' é criada sem erros."""
        t = Transaction(user_id=1, type="despesa",
                        category="alimentacao", amount=100.0)
        assert t.type == "despesa"

    def test_tipo_invalido_levanta_erro(self):
        """Tipo fora de ('receita', 'despesa') deve levantar ValueError."""
        with pytest.raises(ValueError, match="Tipo inválido"):
            Transaction(user_id=1, type="invalido",
                        category="outros", amount=10.0)

    def test_valor_zero_levanta_erro(self):
        """amount <= 0 deve levantar ValueError."""
        with pytest.raises(ValueError):
            Transaction(user_id=1, type="receita", category="outros", amount=0)

    def test_valor_negativo_levanta_erro(self):
        """Valor negativo deve levantar ValueError."""
        with pytest.raises(ValueError):
            Transaction(user_id=1, type="despesa",
                        category="outros", amount=-50)

    def test_date_padrao_hoje(self):
        """Sem date, Transaction usa a data atual no formato YYYY-MM-DD."""
        t = Transaction(user_id=1, type="receita",
                        category="outros", amount=1.0)
        hoje = datetime.now().strftime("%Y-%m-%d")
        assert t.date == hoje

    def test_date_customizada(self):
        """Date fornecida explicitamente é respeitada."""
        t = Transaction(user_id=1, type="despesa",
                        category="lazer", amount=50.0, date="2025-01-15")
        assert t.date == "2025-01-15"

    def test_id_inicializa_como_none(self):
        """id deve ser None antes de ser persistido."""
        t = Transaction(user_id=1, type="receita",
                        category="outros", amount=1.0)
        assert t.id is None

    def test_descricao_padrao_vazia(self):
        """description padrão é string vazia."""
        t = Transaction(user_id=1, type="receita",
                        category="outros", amount=1.0)
        assert t.description == ""

    def test_tipos_validos_disponiveis(self):
        """TYPES contém exatamente 'receita' e 'despesa'."""
        assert "receita" in Transaction.TYPES
        assert "despesa" in Transaction.TYPES

    def test_categorias_receita_presentes(self):
        """Categorias de receita incluem salario e freelance."""
        assert "salario" in Transaction.CATEGORIES["receita"]
        assert "freelance" in Transaction.CATEGORIES["receita"]

    def test_categorias_despesa_presentes(self):
        """Categorias de despesa incluem alimentacao, transporte e lazer."""
        for cat in ("alimentacao", "transporte", "lazer"):
            assert cat in Transaction.CATEGORIES["despesa"]

# ══════════════════════════════════════════════════════════════════════════════
# TESTES DE SERVICES
# ══════════════════════════════════════════════════════════════════════════════

class TestUserService:
    def test_criar_usuario_sucesso(self, mock_db):
        """Cria usuário novo e retorna dict com _id e sem error."""
        mock_db.users.insert_one.return_value = MagicMock(inserted_id="abc123")
        service = UserService()
        user, error = service.create_user_logic(mock_db,
                                                {"username": "pedro", "email": "pedro@bytebank.com", "password": "123"})
        assert error is None
        assert user["username"] == "pedro"
        assert user["email"] == "pedro@bytebank.com"
        assert "_id" in user

    def test_criar_usuario_email_duplicado(self, mock_db):
        """Email já cadastrado deve retornar (None, mensagem de erro)."""
        mock_db.users.find_one.return_value = {"email": "dup@bytebank.com"}
        service = UserService()
        user, error = service.create_user_logic(mock_db,
                                                {"username": "x", "email": "dup@bytebank.com", "password": "123"})
        assert user is None
        assert error == "E-mail já cadastrado."

    def test_criar_usuario_chama_insert_one(self, mock_db):
        """insert_one deve ser chamado exatamente uma vez ao criar usuário."""
        mock_db.users.insert_one.return_value = MagicMock(inserted_id="xyz")
        service = UserService()
        service.create_user_logic(mock_db, {"username": "z", "email": "z@z.com", "password": "abc"})
        mock_db.users.insert_one.assert_called_once()

    def test_criar_usuario_senha_nao_fica_em_texto_puro(self, mock_db):
        """O hash inserido no banco nunca é igual à senha original."""
        mock_db.users.insert_one.return_value = MagicMock(inserted_id="id1")
        service = UserService()
        service.create_user_logic(mock_db, {"username": "z", "email": "z@z.com", "password": "secret"})
        doc_inserido = mock_db.users.insert_one.call_args[0][0]
        assert doc_inserido["password_hash"] != "secret"

    def test_autenticar_credenciais_validas(self, mock_db):
        """authenticate retorna o usuário quando email e senha estão corretos."""
        from werkzeug.security import generate_password_hash
        mock_db.users.find_one.return_value = {
            "_id": "id1",
            "username": "ana",
            "email": "ana@bytebank.com",
            "password_hash": generate_password_hash("senha123"),
        }
        service = UserService()
        user = service.authenticate(mock_db, email="ana@bytebank.com", password="senha123")
        assert user is not None
        assert user["username"] == "ana"

    def test_autenticar_senha_errada_retorna_none(self, mock_db):
        """authenticate retorna None quando a senha não confere."""
        from werkzeug.security import generate_password_hash
        mock_db.users.find_one.return_value = {
            "_id": "id1",
            "username": "ana",
            "email": "ana@bytebank.com",
            "password_hash": generate_password_hash("correta"),
        }
        service = UserService()
        result = service.authenticate(mock_db, email="ana@bytebank.com", password="errada")
        assert result is None

class TestTransactionService:
    def test_criar_transacao_valida(self, mock_db):
        """create_transaction retorna dict sem erro para dados válidos."""
        mock_db.transactions.insert_one.return_value = MagicMock(inserted_id="t1")
        service = TransactionService()
        t, error = service.create_transaction(mock_db, user_id="u1", data={
            "type": "despesa", "category": "alimentacao", "amount": 50.0, "description": "Almoço"
        })
        assert error is None
        assert t["amount"] == 50.0
        assert t["type"] == "despesa"

    def test_criar_transacao_valor_zero_retorna_erro(self, mock_db):
        """amount = 0 deve retornar (None, mensagem de erro)."""
        service = TransactionService()
        t, error = service.create_transaction(mock_db, user_id="u1", data={"amount": 0})
        assert t is None
        assert error is not None

    def test_criar_transacao_valor_negativo_retorna_erro(self, mock_db):
        """amount negativo deve retornar (None, mensagem de erro)."""
        service = TransactionService()
        t, error = service.create_transaction(mock_db, user_id="u1", data={"amount": -100})
        assert t is None
        assert error is not None

    def test_criar_transacao_vincula_user_id(self, mock_db):
        """O user_id passado deve aparecer no documento inserido."""
        mock_db.transactions.insert_one.return_value = MagicMock(inserted_id="t2")
        service = TransactionService()
        service.create_transaction(mock_db, user_id="user_xyz", data={"amount": 10.0})
        doc = mock_db.transactions.insert_one.call_args[0][0]
        assert doc["user_id"] == "user_xyz"

    def test_listar_transacoes_retorna_lista(self, mock_db):
        """get_transactions retorna lista de transações do usuário."""
        mock_db.transactions.find.return_value = [
            {"_id": "t1", "user_id": "u1", "type": "receita", "amount": 1000.0},
            {"_id": "t2", "user_id": "u1", "type": "despesa", "amount": 200.0},
        ]
        service = TransactionService()
        result = service.get_transactions(mock_db, user_id="u1")
        assert len(result) == 2

    def test_listar_transacoes_ids_sao_strings(self, mock_db):
        """Os _id retornados devem ser strings (não ObjectId)."""
        from bson import ObjectId
        mock_db.transactions.find.return_value = [
            {"_id": ObjectId("507f1f77bcf86cd799439011"), "user_id": "u1", "amount": 10.0},
        ]
        service = TransactionService()
        result = service.get_transactions(mock_db, user_id="u1")
        assert isinstance(result[0]["_id"], str)

    def test_listar_transacoes_usuario_sem_transacoes(self, mock_db):
        """get_transactions retorna lista vazia para usuário sem transações."""
        mock_db.transactions.find.return_value = []
        service = TransactionService()
        result = service.get_transactions(mock_db, user_id="u_sem_transacoes")
        assert result == []

    def test_atualizar_transacao_sucesso(self, mock_db):
        """update_transaction atualiza e retorna o documento atualizado."""
        from bson import ObjectId
        oid = ObjectId("507f1f77bcf86cd799439011")
        mock_db.transactions.find_one.return_value = {
            "_id": oid, "amount": 120.0, "description": "Editado"
        }
        service = TransactionService()
        result, error = service.update_transaction(
            mock_db,
            transaction_id="507f1f77bcf86cd799439011",
            data={"amount": 120.0, "description": "Editado"}
        )
        assert error is None
        assert result["amount"] == 120.0

    def test_atualizar_transacao_valor_zero_retorna_erro(self, mock_db):
        """update com amount=0 deve retornar erro."""
        service = TransactionService()
        result, error = service.update_transaction(
            mock_db,
            transaction_id="507f1f77bcf86cd799439011",
            data={"amount": 0}
        )
        assert result is None
        assert error is not None

    def test_atualizar_transacao_sem_campos_validos_retorna_erro(self, mock_db):
        """update sem campos válidos deve retornar erro."""
        service = TransactionService()
        result, error = service.update_transaction(
            mock_db,
            transaction_id="507f1f77bcf86cd799439011",
            data={}
        )
        assert result is None
        assert "Nenhum dado válido" in error

    def test_deletar_transacao_existente(self, mock_db):
        """delete_transaction retorna True quando o documento é removido."""
        mock_db.transactions.delete_one.return_value = MagicMock(deleted_count=1)
        service = TransactionService()
        result = service.delete_transaction(mock_db, "507f1f77bcf86cd799439011")
        assert result is True

    def test_deletar_transacao_inexistente(self, mock_db):
        """delete_transaction retorna False quando nada é removido."""
        mock_db.transactions.delete_one.return_value = MagicMock(deleted_count=0)
        service = TransactionService()
        result = service.delete_transaction(mock_db, "507f1f77bcf86cd799439011")
        assert result is False

# ══════════════════════════════════════════════════════════════════════════════
# TESTES DE ROUTES
# ══════════════════════════════════════════════════════════════════════════════

class TestRotaUsuarios:
    def test_criar_usuario_sucesso(self, client):
        """POST /api/users retorna 201 com dados do novo usuário."""
        with patch("app.routes.user_service") as mock_svc:
            mock_svc.create_user_logic.return_value = (
                {"_id": "id1", "username": "joao", "email": "joao@bytebank.com"},
                None
            )
            resp = client.post("/api/users", json={
                "username": "joao", "email": "joao@bytebank.com", "password": "123"
            })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["username"] == "joao"

    def test_criar_usuario_campos_faltando(self, client):
        """POST /api/users sem campos obrigatórios retorna 400."""
        resp = client.post("/api/users", json={"username": "incompleto"})
        assert resp.status_code == 400

    def test_criar_usuario_email_duplicado(self, client):
        """POST /api/users com email já existente retorna 422."""
        with patch("app.routes.user_service") as mock_svc:
            mock_svc.create_user_logic.return_value = (None, "E-mail já cadastrado.")
            resp = client.post("/api/users", json={
                "username": "x", "email": "dup@bytebank.com", "password": "123"
            })
        assert resp.status_code == 422


class TestRotaLogin:
    def test_login_credenciais_validas(self, client):
        """POST /api/login retorna 200 com token e username."""
        with patch("app.routes.user_service") as mock_svc:
            mock_svc.authenticate.return_value = {"_id": "id1", "username": "ana"}
            resp = client.post("/api/login", json={
                "email": "ana@bytebank.com", "password": "senha123"
            })
        assert resp.status_code == 200
        data = resp.get_json()
        assert "token" in data
        assert data["username"] == "ana"

    def test_login_credenciais_invalidas(self, client):
        """POST /api/login com credenciais erradas retorna 401."""
        with patch("app.routes.user_service") as mock_svc:
            mock_svc.authenticate.return_value = None
            resp = client.post("/api/login", json={
                "email": "nao@existe.com", "password": "errada"
            })
        assert resp.status_code == 401


class TestMiddlewareJWT:
    def test_rota_protegida_sem_token_retorna_401(self, client):
        """GET /api/transactions sem token retorna 401."""
        resp = client.get("/api/transactions")
        assert resp.status_code == 401

    def test_rota_protegida_token_invalido_retorna_401(self, client):
        """GET /api/transactions com token inválido retorna 401."""
        resp = client.get(
            "/api/transactions",
            headers={"Authorization": "Bearer token_invalido"}
        )
        assert resp.status_code == 401

    def test_rota_protegida_sem_bearer_retorna_401(self, client):
        """Authorization sem prefixo 'Bearer ' retorna 401."""
        resp = client.get(
            "/api/transactions",
            headers={"Authorization": "token_sem_bearer"}
        )
        assert resp.status_code == 401

    def test_rota_protegida_com_token_valido_retorna_200(self, client, auth_headers):
        """GET /api/transactions com token válido retorna 200."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.get_transactions.return_value = []
            resp = client.get("/api/transactions", headers=auth_headers)
        assert resp.status_code == 200


class TestRotaTransacoes:
    def test_criar_transacao_com_token_valido(self, client, auth_headers):
        """POST /api/transactions retorna 201 para dados válidos."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.create_transaction.return_value = (
                {"_id": "t1", "type": "despesa", "amount": 50.0}, None
            )
            resp = client.post("/api/transactions", json={
                "type": "despesa", "category": "alimentacao", "amount": 50.0
            }, headers=auth_headers)
        assert resp.status_code == 201

    def test_criar_transacao_erro_retorna_422(self, client, auth_headers):
        """POST /api/transactions com dados inválidos retorna 422."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.create_transaction.return_value = (None, "Valor inválido.")
            resp = client.post("/api/transactions", json={"amount": -10}, headers=auth_headers)
        assert resp.status_code == 422

    def test_listar_transacoes_retorna_lista(self, client, auth_headers):
        """GET /api/transactions retorna lista de transações."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.get_transactions.return_value = [
                {"_id": "t1", "type": "receita", "amount": 1000.0}
            ]
            resp = client.get("/api/transactions", headers=auth_headers)
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_atualizar_transacao_sucesso(self, client, auth_headers):
        """PUT /api/transactions/<id> retorna 200 para atualização válida."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.update_transaction.return_value = (
                {"_id": "t1", "amount": 200.0}, None
            )
            resp = client.put(
                "/api/transactions/507f1f77bcf86cd799439011",
                json={"amount": 200.0},
                headers=auth_headers
            )
        assert resp.status_code == 200

    def test_atualizar_transacao_body_vazio_retorna_400(self, client, auth_headers):
        """PUT /api/transactions/<id> com body JSON vazio ({}) retorna 400."""
        resp = client.put(
            "/api/transactions/507f1f77bcf86cd799439011",
            json={},
            headers=auth_headers
        )
        assert resp.status_code == 400

class TestRotaDashboard:
    def test_dashboard_retorna_resumo_financeiro(self, client, auth_headers):
        """GET /api/dashboard retorna os campos esperados do resumo financeiro."""
        with patch("app.routes.transaction_service") as mock_svc:
            mock_svc.get_dashboard.return_value = {
                "total_receitas": 3000.0,
                "total_despesas": 700.0,
                "saldo": 2300.0,
                "gastos_por_categoria": {"alimentacao": 500.0, "transporte": 200.0},
            }
            resp = client.get("/api/dashboard", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "saldo" in data
        assert "total_receitas" in data
        assert "total_despesas" in data
        assert "gastos_por_categoria" in data

    def test_dashboard_sem_token_retorna_401(self, client):
        """GET /api/dashboard sem token retorna 401."""
        resp = client.get("/api/dashboard")
        assert resp.status_code == 401
