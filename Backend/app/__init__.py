from flask import Flask
from pymongo import MongoClient

# Conexão global com o MongoDB (basta ter o MongoDB rodando na sua máquina)
client = MongoClient("mongodb://localhost:27017/")
db = client["bytebank_db"]


def create_app():
    app = Flask(__name__)

    # Chave secreta para o JWT (Em produção, puxe isso de variáveis de ambiente .env)
    app.config['SECRET_KEY'] = 'uma_chave_muito_secreta_e_complexa'

    @app.route("/")
    def home():
        return "ByteBank backend rodando com MongoDB e JWT!"

    from .routes import bp
    app.register_blueprint(bp)

    return app
