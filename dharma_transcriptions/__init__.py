from flask import Flask

from dharma_transcriptions.database import init_db
from dharma_transcriptions.routes import register_routes


def create_app():
    # Criação e configuração da aplicação Flask
    app = Flask(
        __name__, static_folder='../static', template_folder='../templates'
    )

    # Registra as rotas definidas em routes.py
    register_routes(app)

    # Inicializa o banco de dados (se necessário)
    init_db()

    return app
