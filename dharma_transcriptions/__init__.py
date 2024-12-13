from flask import Flask

def create_app():
    # Criação e configuração da aplicação Flask
    app = Flask(__name__, 
                static_folder="../static", 
                template_folder="../templates")

    # Registra as rotas definidas em routes.py
    from dharma_transcriptions.routes import register_routes
    register_routes(app)

    # Inicializa o banco de dados (se necessário)
    from dharma_transcriptions.database import init_db
    init_db()

    return app
