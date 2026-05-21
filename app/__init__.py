from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "ByteBank backend rodando!"

    from .routes import bp
    app.register_blueprint(bp)

    return app