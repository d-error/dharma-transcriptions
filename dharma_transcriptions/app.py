from dharma_transcriptions import create_app

# Cria o app usando a fábrica configurada no __init__.py
app = create_app()

if __name__ == "__main__":
    # Inicia o servidor Flask
    app.run(host="0.0.0.0", port=5000, debug=True)
