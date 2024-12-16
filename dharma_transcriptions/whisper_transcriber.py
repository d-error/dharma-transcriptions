import os
import whisper


class WhisperTranscriber:
    def __init__(self, model_name="base", trained_model_path=None):
        """
        Inicializa o transcritor Whisper.
        :param model_name: Nome do modelo Whisper a ser carregado.
        :param trained_model_path: Caminho para o modelo ajustado, se existir.
        """
        print(f"[INFO] Inicializando WhisperTranscriber com o modelo '{model_name}'...")
        if trained_model_path and os.path.exists(trained_model_path):
            print(f"[INFO] Carregando modelo ajustado de: {trained_model_path}")
            self.model = whisper.load_model(trained_model_path)
        else:
            print("[INFO] Carregando modelo padrão do Whisper...")
            self.model = whisper.load_model(model_name)
        print("[INFO] Modelo carregado com sucesso.")

    def transcribe_audio(self, audio_path):
        """
        Transcreve o áudio usando o modelo Whisper.
        :param audio_path: Caminho para o arquivo de áudio.
        :return: Transcrição gerada.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"[ERRO] Arquivo de áudio não encontrado: {audio_path}")
        print(f"[INFO] Transcrevendo áudio: {audio_path}...")
        result = self.model.transcribe(audio_path, fp16=False)
        print("[INFO] Transcrição concluída.")
        return result["text"], result["segments"]

    def save_transcription(self, text, segments, output_path):
        """
        Salva a transcrição em dois formatos: texto simples e SRT.
        :param text: Transcrição completa.
        :param segments: Segmentos da transcrição (usado para SRT).
        :param output_path: Caminho para salvar os arquivos de saída.
        """
        os.makedirs(output_path, exist_ok=True)

        # Salvar texto simples
        text_path = os.path.join(output_path, "transcription.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[INFO] Transcrição salva em: {text_path}")

        # Salvar legendas em formato SRT
        srt_path = os.path.join(output_path, "subtitles.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, segment in enumerate(segments):
                start_time = self._format_time(segment["start"])
                end_time = self._format_time(segment["end"])
                text = segment["text"]
                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        print(f"[INFO] Legendas SRT salvas em: {srt_path}")

    def fine_tune(self, audio_path, corrected_text):
        """
        Placeholder para ajuste fino (fine-tuning) do modelo.
        :param audio_path: Caminho para o áudio usado no treinamento.
        :param corrected_text: Transcrição corrigida correspondente ao áudio.
        """
        print("[INFO] Função de ajuste fino ainda a ser implementada...")
        # Esta é uma função avançada que requer o treinamento com Whisper
        # e ferramentas de ajuste fino de modelos.

    @staticmethod
    def _format_time(seconds):
        """
        Formata o tempo em segundos para o formato SRT.
        :param seconds: Tempo em segundos.
        :return: Tempo formatado como HH:MM:SS,mmm.
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
