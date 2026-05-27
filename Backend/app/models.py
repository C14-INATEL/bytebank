from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Representa um usuário do sistema estruturado para segurança."""

    def __init__(self, username, email, password):
        self.id = None
        self.username = username
        self.email = email
        # Armazena a senha já criptografada em formato hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida em texto puro bate com o hash do banco."""
        return check_password_hash(self.password_hash, password)


class Transaction:
    """
    Representa uma transação financeira (receita ou despesa).

    type     : 'receita' | 'despesa'
    category : ex. 'salario', 'alimentacao', 'transporte', 'lazer', etc.
    """

    TYPES = ("receita", "despesa")

    CATEGORIES = {
        "receita": ("salario", "freelance", "investimento", "outros"),
        "despesa": ("alimentacao", "transporte", "lazer", "contas", "saude", "educacao", "outros"),
    }

    def __init__(self, user_id, type, category, amount, description="", date=None):
        if type not in self.TYPES:
            raise ValueError(
                f"Tipo inválido: '{type}'. Use 'receita' ou 'despesa'.")
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        self.id = None
        self.user_id = user_id
        self.type = type
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")
