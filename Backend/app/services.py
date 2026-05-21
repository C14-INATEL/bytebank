from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash


class UserService:
    def create_user_logic(self, db, user_data):
        email = user_data.get("email")
        username = user_data.get("username")
        password = user_data.get("password")

        # Verifica se o email já existe no MongoDB
        if db.users.find_one({"email": email}):
            return None, "E-mail já cadastrado."

        novo_usuario = {
            "username": username,
            "email": email,
            "password_hash": generate_password_hash(password)
        }

        result = db.users.insert_one(novo_usuario)
        novo_usuario["_id"] = str(result.inserted_id)
        return novo_usuario, None

    def authenticate(self, db, email, password):
        user = db.users.find_one({"email": email})
        if not user or not check_password_hash(user["password_hash"], password):
            return None
        user["_id"] = str(user["_id"])
        return user


class TransactionService:
    def create_transaction(self, db, user_id, data):
        """Registra uma nova receita ou despesa no MongoDB."""
        amount = data.get("amount")
        if not amount or amount <= 0:
            return None, "O valor deve ser um número positivo."

        transacao = {
            # Vincula a transação ao ID do usuário do Token
            "user_id": str(user_id),
            "type": data.get("type", "receita"),
            "category": data.get("category", "outros"),
            "amount": amount,
            "description": data.get("description", ""),
            "date": data.get("date")
        }

        result = db.transactions.insert_one(transacao)
        transacao["_id"] = str(result.inserted_id)
        return transacao, None

    def get_transactions(self, db, user_id):
        """Busca todas as transações daquele usuário específico."""
        transacoes = list(db.transactions.find({"user_id": str(user_id)}))
        # Converte o ObjectId do Mongo para string para o JSON do React não quebrar
        for t in transacoes:
            t["_id"] = str(t["_id"])
        return transacoes

    def update_transaction(self, db, transaction_id, data):
        """Atualiza campos de uma transação existente no MongoDB."""
        query = {"_id": ObjectId(transaction_id)}

        # Prepara os campos que serão alterados
        update_fields = {}
        if "amount" in data:
            if data["amount"] <= 0:
                return None, "O valor deve ser positivo."
            update_fields["amount"] = data["amount"]
        if "description" in data:
            update_fields["description"] = data["description"]
        if "category" in data:
            update_fields["category"] = data["category"]
        if "date" in data:
            update_fields["date"] = data["date"]

        if not update_fields:
            return None, "Nenhum dado válido para atualização."

        # Atualiza no Mongo
        db.transactions.update_one(query, {"$set": update_fields})

        # Busca a transação atualizada para retornar
        updated = db.transactions.find_one(query)
        if updated:
            updated["_id"] = str(updated["_id"])
        return updated, None

    def delete_transaction(self, db, transaction_id):
        """Remove uma transação pelo ID no MongoDB."""
        result = db.transactions.delete_one({"_id": ObjectId(transaction_id)})
        return result.deleted_count > 0

    def get_dashboard(self, db, user_id):
        """Retorna o resumo financeiro do usuário agrupado do MongoDB."""
        # Busca todas as transações daquele usuário específico
        transactions = list(db.transactions.find({"user_id": str(user_id)}))

        total_receitas = sum(t["amount"]
                             for t in transactions if t["type"] == "receita")
        total_despesas = sum(t["amount"]
                             for t in transactions if t["type"] == "despesa")

        gastos_por_categoria = {}
        for t in transactions:
            if t["type"] == "despesa":
                cat = t.get("category", "outros")
                gastos_por_categoria[cat] = gastos_por_categoria.get(
                    cat, 0.0) + t["amount"]

        return {
            "total_receitas": total_receitas,
            "total_despesas": total_despesas,
            "saldo": total_receitas - total_despesas,
            "gastos_por_categoria": gastos_por_categoria,
        }
