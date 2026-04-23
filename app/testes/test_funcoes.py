import pytest
from unittest.mock import MagicMock
from app.services import UserService


@pytest.fixture
def mock_db():
    return MagicMock()


# teste 1: Verificar se a função de criação de usuário retorna um objeto válido
def test_1_criar_usuario_com_sucesso(mock_db):
    service = UserService()
    dados = {"username": "pedro",
             "email": "pedro@bytebank.com", "password": "123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.username == "pedro"

# teste 2: Verificar se a função de criação de usuário percebe um email invalido


def test_2_criar_usuario_email_invalido(mock_db):
    service = UserService()
    dados = {"username": "error", "email": "email_ruim.com", "password": "123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is None

# teste 3: Verificar se a função de busca de usuário retorna None para um ID inexistente


def test_3_buscar_usuario_inexistente(mock_db):
    mock_db.query().filter().first.return_value = None
    service = UserService()
    user = service.get_user_by_id(mock_db, 999)
    assert user is None


# teste 4: Verificar se a função de criação de usuário chama o método add do mock db
def test_4_verificar_se_db_foi_chamado(mock_db):
    service = UserService()
    dados = {"username": "teste", "email": "teste@teste.com", "password": "123"}
    service.create_user_logic(mock_db, dados)
    assert mock_db.add.called



# Teste 5: Verificar se o usuário criado possui o email correto
def test_5_criar_usuario_verifica_email(mock_db):
    service = UserService()
    dados = {"username": "ana", "email": "ana@bytebank.com", "password": "senha123"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.email == "ana@bytebank.com"


# Teste 6: Verificar se o usuário criado possui a senha correta
def test_6_criar_usuario_verifica_senha(mock_db):
    service = UserService()
    dados = {"username": "joao", "email": "joao@bytebank.com", "password": "minhasenha"}
    resultado = service.create_user_logic(mock_db, dados)
    assert resultado is not None
    assert resultado.password == "minhasenha"


# Teste 7: Verificar se a criação sem DB não atribui ID ao usuário
def test_7_criar_usuario_sem_db_nao_atribui_id():
    service = UserService()
    dados = {"username": "maria", "email": "maria@bytebank.com", "password": "abc"}
    resultado = service.create_user_logic(None, dados)
    assert resultado is not None
    assert resultado.id is None


# Teste 8: Verificar se a busca de usuário retorna o objeto correto quando encontrado no DB
def test_8_buscar_usuario_existente_retorna_objeto(mock_db):
    usuario_mock = User(username="carlos", email="carlos@bytebank.com", password="xyz")
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
    dados = {"username": "lucas", "email": "lucas@bytebank.com", "password": "123"}

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
 
    transaction, error = service.create_transaction(mock_db, user_id=1, data=dados)
 
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
    receita = Transaction(user_id=1, type="receita", category="salario", amount=3000.0)
    despesa1 = Transaction(user_id=1, type="despesa", category="alimentacao", amount=500.0)
    despesa2 = Transaction(user_id=1, type="despesa", category="transporte", amount=200.0)
 
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