from datetime import datetime


class User:
    """Representa um usuário do sistema."""

    def __init__(self, username, email, password):
        self.id = None
        self.username = username
        self.email = email
        self.password = password  # Em produção: hash com bcrypt


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
            raise ValueError(f"Tipo inválido: '{type}'. Use 'receita' ou 'despesa'.")
        if amount <= 0:
            raise ValueError("O valor da transação deve ser positivo.")

        self.id = None
        self.user_id = user_id
        self.type = type
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")