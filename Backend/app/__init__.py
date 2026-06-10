import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

_mongo_uri = os.getenv('MONGO_URI', '')
_client = MongoClient(_mongo_uri) if _mongo_uri else None
db = _client[os.getenv('MONGO_DB', 'bytebank_db')] if _client else None

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-local-desenvolvimento')

    @app.route("/")
    def home():
        return "ByteBank backend rodando com MongoDB e JWT!"

    from .routes import bp
    app.register_blueprint(bp)

    return app
