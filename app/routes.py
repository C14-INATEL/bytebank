from flask import Blueprint, request, jsonify
from .services import UserService, TransactionService

bp = Blueprint("api", __name__, url_prefix="/api")

user_service = UserService()
transaction_service = TransactionService()


# ── Autenticação e Usuários ───────────────────────────────────────────────────

@bp.route("/users", methods=["POST"])
def create_user():
    """Cadastro de novo usuário."""
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password")):
        return jsonify({"error": "Campos obrigatórios: username, email, password"}), 400

    user, error = _wrap_user_create(data)
    if error:
        return jsonify({"error": error}), 422

    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201


@bp.route("/login", methods=["POST"])
def login():
    """Autenticação do usuário."""
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Campos obrigatórios: email, password"}), 400

    user = user_service.authenticate(db=None, email=data["email"], password=data["password"])
    if user is None:
        return jsonify({"error": "Credenciais inválidas."}), 401

    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200


@bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Busca dados de um usuário pelo ID."""
    user = user_service.get_user_by_id(db=None, user_id=user_id)
    if user is None:
        return jsonify({"error": "Usuário não encontrado."}), 404
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200


# ── Transações (Receitas e Despesas) ─────────────────────────────────────────

@bp.route("/users/<int:user_id>/transactions", methods=["POST"])
def create_transaction(user_id):
    """Registra uma nova receita ou despesa."""
    data = request.get_json()
    if not data or not all(k in data for k in ("type", "amount")):
        return jsonify({"error": "Campos obrigatórios: type, amount"}), 400

    transaction, error = transaction_service.create_transaction(db=None, user_id=user_id, data=data)
    if error:
        return jsonify({"error": error}), 422

    return jsonify({
        "id": transaction.id,
        "type": transaction.type,
        "category": transaction.category,
        "amount": transaction.amount,
        "description": transaction.description,
        "date": transaction.date,
    }), 201


@bp.route("/users/<int:user_id>/transactions", methods=["GET"])
def list_transactions(user_id):
    """Lista todas as transações do usuário. Aceita ?type=receita ou ?type=despesa."""
    type_filter = request.args.get("type")
    transactions = transaction_service.get_transactions(db=None, user_id=user_id, type_filter=type_filter)
    result = [
        {
            "id": t.id,
            "type": t.type,
            "category": t.category,
            "amount": t.amount,
            "description": t.description,
            "date": t.date,
        }
        for t in transactions
    ]
    return jsonify(result), 200


@bp.route("/transactions/<int:transaction_id>", methods=["PUT"])
def update_transaction(transaction_id):
    """Edita uma transação existente."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado."}), 400

    transaction, error = transaction_service.update_transaction(db=None, transaction_id=transaction_id, data=data)
    if error:
        return jsonify({"error": error}), 422

    return jsonify({
        "id": transaction.id,
        "type": transaction.type,
        "category": transaction.category,
        "amount": transaction.amount,
        "description": transaction.description,
        "date": transaction.date,
    }), 200


@bp.route("/transactions/<int:transaction_id>", methods=["DELETE"])
def delete_transaction(transaction_id):
    """Exclui uma transação pelo ID."""
    deleted = transaction_service.delete_transaction(db=None, transaction_id=transaction_id)
    if not deleted:
        return jsonify({"error": "Transação não encontrada."}), 404
    return jsonify({"message": "Transação removida com sucesso."}), 200


# ── Dashboard ─────────────────────────────────────────────────────────────────

@bp.route("/users/<int:user_id>/dashboard", methods=["GET"])
def dashboard(user_id):
    """
    Retorna o resumo financeiro do usuário:
    saldo atual, total de receitas, total de despesas e gastos por categoria.
    """
    summary = transaction_service.get_dashboard(db=None, user_id=user_id)
    return jsonify(summary), 200


# ── Helpers internos ──────────────────────────────────────────────────────────

def _wrap_user_create(data):
    user = user_service.create_user_logic(db=None, user_data=data)
    if user is None:
        return None, "E-mail inválido ou campos obrigatórios ausentes."
    return user, None
