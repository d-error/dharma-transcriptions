import os

import torch
import whisper


def load_model(fine_tuned=False):
    model = whisper.load_model('base')

    if fine_tuned:
        """
    Carrega o modelo Whisper treinado (fine-tuned).
    """
        TRAINED_MODEL_PATH = os.path.join(
            'trained_models', 'whisper_finetuned.pt'
        )

        if not os.path.exists(TRAINED_MODEL_PATH):
            raise FileNotFoundError(
                f'Modelo treinado não encontrado: {TRAINED_MODEL_PATH}'
            )

        print('[INFO] Carregando modelo treinado...')
        model.load_state_dict(torch.load(TRAINED_MODEL_PATH))
        print('[INFO] Modelo treinado carregado com sucesso.')
        return model
    else:
        """
    Carrega o modelo base do Whisper e habilita o cálculo de gradientes.
    """
        print('[INFO] Carregando o modelo base Whisper...')
        # Habilitar cálculo de gradientes para ajuste fino
        for param in model.parameters():
            param.requires_grad = True

        print('[INFO] Modelo base Whisper carregado com sucesso.')
        return model
