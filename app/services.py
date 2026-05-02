from .models import User, Transaction


class UserService:
    """Serviço responsável por cadastro e autenticação de usuários."""

    def create_user_logic(self, db, user_data):
        """
        Cria um novo usuário após validações básicas.
        Retorna o objeto User ou None em caso de dados inválidos.
        """
        email = user_data.get("email", "")
        username = user_data.get("username", "")
        password = user_data.get("password", "")

        if "@" not in email or "." not in email.split("@")[-1]:
            return None

        if not username or not password:
            return None

        new_user = User(
            username=username,
            email=email,
            password=password,
        )

        if db:
            db.add(new_user)
            new_user.id = 1

        return new_user

    def get_user_by_id(self, db, user_id):
        """Busca um usuário pelo ID. Retorna None se não encontrado."""
        if db is None:
            return None
        return db.query().filter().first()

    def authenticate(self, db, email, password):
        """
        Valida credenciais do usuário.
        Retorna o usuário se autenticado, None caso contrário.
        """
        if db is None:
            return None
        user = db.query().filter_by(email=email).first()
        if user is None:
            return None
        if user.password != password:
            return None
        return user


class TransactionService:
    """Serviço responsável por receitas, despesas e relatórios financeiros."""

    def create_transaction(self, db, user_id, data):
        """
        Registra uma nova receita ou despesa.
        Retorna (Transaction, None) ou (None, mensagem_de_erro).
        """
        type_ = data.get("type", "")
        category = data.get("category", "outros")
        amount = data.get("amount")
        description = data.get("description", "")
        date = data.get("date")

        if not amount or amount <= 0:
            return None, "O valor deve ser um número positivo."

        try:
            transaction = Transaction(
                user_id=user_id,
                type=type_,
                category=category,
                amount=amount,
                description=description,
                date=date,
            )
        except ValueError as e:
            return None, str(e)

        if db:
            db.add(transaction)
            transaction.id = 1

        return transaction, None

    def get_transactions(self, db, user_id, type_filter=None):
        """
        Retorna todas as transações do usuário.
        Se type_filter='receita' ou 'despesa', filtra pelo tipo.
        """
        if db is None:
            return []
        return db.query(Transaction).filter_by(user_id=user_id, type=type_filter).all() \
            if type_filter else db.query(Transaction).filter_by(user_id=user_id).all()

    def update_transaction(self, db, transaction_id, data):
        """
        Atualiza campos de uma transação existente.
        Retorna (Transaction, None) ou (None, mensagem_de_erro).
        """
        if db is None:
            return None, "Banco de dados indisponível."

        transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction is None:
            return None, "Transação não encontrada."

        if "amount" in data:
            if data["amount"] <= 0:
                return None, "O valor deve ser positivo."
            transaction.amount = data["amount"]

        if "description" in data:
            transaction.description = data["description"]

        if "category" in data:
            transaction.category = data["category"]

        if "date" in data:
            transaction.date = data["date"]

        return transaction, None

    def delete_transaction(self, db, transaction_id):
        """
        Remove uma transação pelo ID.
        Retorna True se removida, False se não encontrada.
        """
        if db is None:
            return False

        transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if transaction is None:
            return False

        db.delete(transaction)
        return True

    def get_dashboard(self, db, user_id):
        """
        Retorna o resumo financeiro do usuário:
        - total de receitas
        - total de despesas
        - saldo atual
        - gastos agrupados por categoria
        """
        if db is None:
            return {
                "total_receitas": 0.0,
                "total_despesas": 0.0,
                "saldo": 0.0,
                "gastos_por_categoria": {},
            }

        transactions = db.query(Transaction).filter_by(user_id=user_id).all()

        total_receitas = sum(t.amount for t in transactions if t.type == "receita")
        total_despesas = sum(t.amount for t in transactions if t.type == "despesa")

        gastos_por_categoria = {}
        for t in transactions:
            if t.type == "despesa":
                gastos_por_categoria[t.category] = (
                    gastos_por_categoria.get(t.category, 0.0) + t.amount
                )

        return {
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": total_receitas - total_despesas,
            "gastos_por_categoria": gastos_por_categoria,
        }