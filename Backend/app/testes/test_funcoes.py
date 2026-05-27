<<<<<<< HEAD
"""
Testes unitários do ByteBank Backend
Cobertura: models, services, routes (via Flask test client)
"""
import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# ── Importações dos módulos testados ──────────────────────────────────────────
=======
import pytest
from unittest.mock import MagicMock

>>>>>>> 726a406b42a770a0562d69c46d8a948baf598dcc
from app.models import User, Transaction
from app.services import UserService, TransactionService


<<<<<<< HEAD
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
=======
@pytest.fixture
def mock_db():
    return MagicMock()


# Teste 1: Verificar se a função de criação de usuário retorna um objeto válido
def test_1_criar_usuario_com_sucesso(mock_db):
    service = UserService()
    dados = {"username": "pedro",
             "email": "pedro@bytebank.com", "password": "123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.username == "pedro"


# Teste 2: Verificar se a função de criação de usuário percebe um email invalido
def test_2_criar_usuario_email_invalido(mock_db):
    service = UserService()
    dados = {"username": "error", "email": "email_ruim.com", "password": "123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is None


# Teste 3: Verificar se a função de busca de usuário retorna None para um ID inexistente
def test_3_buscar_usuario_inexistente(mock_db):
    mock_db.query().filter().first.return_value = None
    service = UserService()
    user = service.get_user_by_id(mock_db, 999)
    assert user is None


# Teste 4: Verificar se a função de criação de usuário chama o método add do mock db
def test_4_verificar_se_db_foi_chamado(mock_db):
    service = UserService()
    dados = {"username": "teste", "email": "teste@teste.com", "password": "123"}
    service.create_user_logic(mock_db, dados)
    assert mock_db.add.called


# Teste 5: Verificar se o usuário criado possui o email correto
def test_5_criar_usuario_verifica_email(mock_db):
    service = UserService()
    dados = {"username": "ana",
             "email": "ana@bytebank.com", "password": "senha123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.email == "ana@bytebank.com"


# Teste 6: Verificar se o usuário criado possui a senha correta
def test_6_criar_usuario_verifica_senha(mock_db):
    service = UserService()
    dados = {"username": "joao", "email": "joao@bytebank.com",
             "password": "minhasenha"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.password == "minhasenha"


# Teste 7: Verificar se a criação sem DB não atribui ID ao usuário
def test_7_criar_usuario_sem_db_nao_atribui_id():
    service = UserService()
    dados = {"username": "maria",
             "email": "maria@bytebank.com", "password": "abc"}
    resultado = service.create_user_logic(None, dados)
    assert resultado is not None
    assert resultado.id is None


# Teste 8: Verificar se a busca de usuário retorna o objeto correto quando encontrado no DB
def test_8_buscar_usuario_existente_retorna_objeto(mock_db):
    usuario_mock = User(username="carlos",
                        email="carlos@bytebank.com", password="xyz")
    usuario_mock.id = 42
    mock_db.query().filter().first.return_value = usuario_mock

    service = UserService()
    resultado = service.get_user_by_id(mock_db, 42)

    assert resultado is not None
    assert resultado.username == "carlos"
    assert resultado.id == 42


# Teste 9: Email inválido não deve chamar db.add
def test_9_email_invalido_nao_chama_add(mock_db):
    service = UserService()
    dados = {"username": "erro", "email": "emailinvalido.com", "password": "123"}

    resultado = service.create_user_logic(mock_db, dados)

    assert resultado is None
    mock_db.add.assert_not_called()


# Teste 10: Buscar usuário sem DB deve retornar None
def test_10_buscar_usuario_sem_db_retorna_none():
    service = UserService()

    resultado = service.get_user_by_id(None, 1)

    assert resultado is None


# Teste 11: Criar usuário com DB deve atribuir ID = 1
def test_11_criar_usuario_com_db_atribui_id(mock_db):
    service = UserService()
    dados = {"username": "lucas",
             "email": "lucas@bytebank.com", "password": "123"}

    resultado = service.create_user_logic(mock_db, dados)

    assert resultado is not None
    assert resultado.id == 1


# Teste 12: Verificar se db.add recebeu um objeto User correto
def test_12_db_add_recebe_objeto_user(mock_db):
    service = UserService()
    dados = {"username": "bia", "email": "bia@bytebank.com", "password": "456"}

    service.create_user_logic(mock_db, dados)

    usuario_passado = mock_db.add.call_args[0][0]

    assert isinstance(usuario_passado, User)
    assert usuario_passado.username == "bia"


# ── Testes de TransactionService ─────────────────────────────────────────────

# Teste 13: Registrar uma despesa chama db.add e retorna transação correta
def test_13_registrar_despesa_chama_db_add(mock_db):
    """
    Garante que TransactionService.create_transaction chama db.add com uma
    Transaction do tipo 'despesa' e retorna os dados corretos, sem erro.
    Contexto: usuário registra um gasto de alimentação no sistema de finanças pessoais.
    """
    service = TransactionService()
    dados = {
        "type": "despesa",
        "category": "alimentacao",
        "amount": 85.50,
        "description": "Mercado semanal",
        "date": "2026-04-23",
    }

    transaction, error = service.create_transaction(
        mock_db, user_id=1, data=dados)

    assert error is None
    assert transaction is not None
    assert transaction.type == "despesa"
    assert transaction.category == "alimentacao"
    assert transaction.amount == 85.50
    mock_db.add.assert_called_once()


# Teste 14: Dashboard retorna saldo correto com base nas transações mockadas
def test_14_dashboard_calcula_saldo_corretamente(mock_db):
    """
    Garante que TransactionService.get_dashboard calcula corretamente o saldo
    (receitas - despesas) e os gastos por categoria usando transações mockadas.
    Contexto: visualização do painel financeiro do usuário.
    """
    receita = Transaction(user_id=1, type="receita",
                          category="salario", amount=3000.0)
    despesa1 = Transaction(user_id=1, type="despesa",
                           category="alimentacao", amount=500.0)
    despesa2 = Transaction(user_id=1, type="despesa",
                           category="transporte", amount=200.0)

    mock_db.query(Transaction).filter_by(user_id=1).all.return_value = [
        receita, despesa1, despesa2
    ]

    service = TransactionService()
    resultado = service.get_dashboard(mock_db, user_id=1)

    assert resultado["total_receitas"] == 3000.0
    assert resultado["total_despesas"] == 700.0
    assert resultado["saldo"] == 2300.0
    assert resultado["gastos_por_categoria"]["alimentacao"] == 500.0
    assert resultado["gastos_por_categoria"]["transporte"] == 200.0


# Teste 15: Atualizar transação existente usando mock do banco
def test_15_update_transaction_com_mock(mock_db):
    service = TransactionService()

    transacao_mock = Transaction(
        user_id=1,
        type="despesa",
        category="alimentacao",
        amount=50.0,
        description="Lanche",
        date="2026-04-10"
    )
    transacao_mock.id = 1

    mock_db.query(Transaction).filter_by(
        id=1).first.return_value = transacao_mock

    dados = {
        "amount": 120.0,
        "description": "Compra no mercado",
        "category": "alimentacao",
        "date": "2026-04-25"
    }

    resultado, erro = service.update_transaction(mock_db, 1, dados)

    assert erro is None
    assert resultado.amount == 120.0
    assert resultado.description == "Compra no mercado"
    assert resultado.date == "2026-04-25"
    mock_db.query.assert_any_call(Transaction)


# Teste 16: Deletar transação existente usando mock do banco
def test_16_delete_transaction_com_mock(mock_db):
    service = TransactionService()

    transacao_mock = Transaction(
        user_id=1,
        type="despesa",
        category="transporte",
        amount=30.0,
        description="Uber",
        date="2026-04-25"
    )
    transacao_mock.id = 1

    mock_db.query(Transaction).filter_by(
        id=1).first.return_value = transacao_mock

    resultado = service.delete_transaction(mock_db, 1)

    assert resultado is True
    mock_db.delete.assert_called_once_with(transacao_mock)
>>>>>>> 726a406b42a770a0562d69c46d8a948baf598dcc
