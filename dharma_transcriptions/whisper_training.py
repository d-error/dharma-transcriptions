import os
import torch
import whisper

# Caminho para salvar o modelo treinado
TRAINED_MODEL_PATH = os.path.join("trained_models", "whisper_finetuned.pt")

# Caminho dos dados de treinamento
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "TREINAMENTO"))
BRUTOS_PATH = os.path.join(BASE_PATH, "dados_brutos")
CORRIGIDOS_PATH = os.path.join(BASE_PATH, "referencia_corrigida")


def load_base_model():
    print("[INFO] Carregando o modelo base Whisper...")
    model = whisper.load_model("base")
    print("[INFO] Modelo base Whisper carregado com sucesso.")
    return model


def fine_tune_model(model, training_pairs):
    print("[INFO] Iniciando ajuste fino do modelo...")

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Simulação de ajuste fino
    for epoch in range(2):  # Simular 2 épocas
        print(f"[INFO] Época {epoch + 1}")
        for bruto_path, corrigido_path in training_pairs:
            print(f"[DEBUG] Treinando com: {bruto_path} e {corrigido_path}")
            # Simular perda
            loss = torch.tensor(0.1)  # Substituir por cálculo real de perda
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    print("[INFO] Fine-tuning concluído.")
    return model


def save_finetuned_model(model):
    print(f"[DEBUG] Tentando salvar o modelo em: {TRAINED_MODEL_PATH}")
    os.makedirs(os.path.dirname(TRAINED_MODEL_PATH), exist_ok=True)
    torch.save(model.state_dict(), TRAINED_MODEL_PATH)
    print(f"[INFO] Modelo salvo com sucesso em: {TRAINED_MODEL_PATH}")


if __name__ == "__main__":
    try:
        # Verificar dados de treinamento
        training_pairs = []
        for bruto in os.listdir(BRUTOS_PATH):
            base_name = os.path.splitext(bruto)[0]
            corrigido = os.path.join(CORRIGIDOS_PATH, f"{base_name}.txt")
            if os.path.exists(corrigido):
                training_pairs.append((os.path.join(BRUTOS_PATH, bruto), corrigido))

        if not training_pairs:
            raise ValueError("[ERRO] Nenhum par válido para treinamento.")

        print(f"[INFO] Total de pares de treinamento: {len(training_pairs)}")

        # Carregar modelo base
        model = load_base_model()

        # Ajustar modelo
        finetuned_model = fine_tune_model(model, training_pairs)

        # Salvar modelo ajustado
        save_finetuned_model(finetuned_model)

        print("[INFO] Treinamento finalizado com sucesso!")
    except Exception as e:
        print(f"[ERRO] Ocorreu um erro: {e}")
