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
