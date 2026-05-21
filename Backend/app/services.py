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
        # Busca todas as transações daquele usuário específico
        transacoes = list(db.transactions.find({"user_id": str(user_id)}))
        # Converte o ObjectId do Mongo para string para o JSON do React
        for t in transacoes:
            t["_id"] = str(t["_id"])
        return transacoes
