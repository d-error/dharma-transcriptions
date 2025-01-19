import os

import torch
import whisper

from dharma_transcriptions.config import Config


def load_model(fine_tuned=False):
    model = whisper.load_model(Config.WHISPER_MODEL)
    BASE_PATH = Config.BASE_PATH

    if fine_tuned:
        """
    Carrega o modelo Whisper treinado (fine-tuned).
    """
        TRAINED_MODEL_PATH = os.path.join(
            BASE_PATH, 'trained_models', 'whisper_finetuned.pt'
        )

        try:
            print('[INFO] Carregando modelo treinado...')
            model.load_state_dict(torch.load(TRAINED_MODEL_PATH))
            print('[INFO] Modelo treinado carregado com sucesso.')
            return model

        except FileNotFoundError:
            print(
                '[WARNING] Modelo treinado não encontrado em:',
                '{TRAINED_MODEL_PATH}. Usando modelo padrão.',
            )
            return turn_required_grads(model)

    else:
        return turn_required_grads(model)


def turn_required_grads(model):
    """
    Retorna o modelo base do Whisper com o cálculo de gradientes habilitado.
    """
    print(f'[INFO] Carregando o modelo Whisper {Config.WHISPER_MODEL} ...')
    # Habilitar cálculo de gradientes para ajuste fino
    # TODO: testar se ele realmente está alterando esses parametros pra True
    # e verificar o que significa isso. (Diego)
    for param in model.parameters():
        param.requires_grad = True

    print(
        f'[INFO] Modelo Whisper {Config.WHISPER_MODEL} carregado com sucesso.'
    )
    return model


if __name__ == '__main__':
    model = load_model(True)
