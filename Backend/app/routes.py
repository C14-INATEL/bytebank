import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, current_app

from .services import UserService, TransactionService
from . import db  # Importa o db configurado no __init__.py

bp = Blueprint("api", __name__, url_prefix="/api")
user_service = UserService()
transaction_service = TransactionService()

# ── Middleware de Segurança JWT ───────────────────────────────────────────────


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token ausente ou formato inválido!"}), 401

        try:
            token = token.split(" ")[1]  # Remove a palavra "Bearer "
            data = jwt.decode(
                token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except Exception:
            return jsonify({"error": "Token inválido ou expirado!"}), 401

        return f(current_user_id, *args, **kwargs)
    return decorated

# ── Rotas Abertas (Não precisam de Token) ────────────────────────────────────


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = user_service.authenticate(
        db, email=data["email"], password=data["password"])

    if not user:
        return jsonify({"error": "Credenciais inválidas."}), 401

    # Gera o Token com validade de 2 horas
    token = jwt.encode({
        'user_id': user["_id"],
        'exp': datetime.utcnow() + timedelta(hours=2)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({"token": token, "username": user["username"]}), 200

# ── Rotas Protegidas (Exigem o Token) ────────────────────────────────────────


@bp.route("/transactions", methods=["POST"])
@token_required  # <- O guarda-costas em ação!
def create_transaction(current_user_id):
    """user_id não vem mais da URL, vem de dentro do token verificado."""
    data = request.get_json()
    transaction, error = transaction_service.create_transaction(
        db, user_id=current_user_id, data=data)

    if error:
        return jsonify({"error": error}), 422
    return jsonify(transaction), 201


@bp.route("/transactions", methods=["GET"])
@token_required
def list_transactions(current_user_id):
    transactions = transaction_service.get_transactions(
        db, user_id=current_user_id)
    return jsonify(transactions), 200
