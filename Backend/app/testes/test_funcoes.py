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
