from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

# Sua conexão exata que já sabemos que funciona
uri = "mongodb+srv://henriquecastro2626:9VtpioyGVzc3nYo6@cluster0.ejccf4y.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["bytebank_db"]


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config['SECRET_KEY'] = 'uma_chave_muito_secreta_e_complexa'

    @app.route("/")
    def home():
        return "ByteBank backend rodando com MongoDB e JWT!"

    # pro Flask usar o routes.py!
    from .routes import bp
    app.register_blueprint(bp)

    return app
