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
