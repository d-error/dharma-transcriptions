import os

from dharma_transcriptions.utils import format_time
from dharma_transcriptions.whisper_core import load_model


def transcribe_audio_and_generate_subtitles(
    audio_file, video_title, file_folder
):
    if not os.path.exists(audio_file):
        raise FileNotFoundError(
            f'Arquivo de áudio não encontrado: {audio_file}'
        )
    print('[INFO] Carregando modelo Whisper...')
    model = load_model()
    print('[INFO] Modelo Whisper carregado com sucesso.')

    print(f'[INFO] Transcrevendo o arquivo de áudio: {audio_file}')
    result = model.transcribe(audio_file, fp16=False)
    print('[INFO] Transcrição concluída com sucesso.')

    transcript_file_path = save_transcription(file_folder, video_title, result)
    subtitle_file_path = save_subtitle(file_folder, video_title, result)

    return transcript_file_path, subtitle_file_path


def save_transcription(file_folder, video_title, result):
    transcript_file_path = os.path.join(file_folder, video_title + '.txt')
    with open(transcript_file_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])
    print(f'[INFO] Transcrição salva em: {transcript_file_path}')
    return transcript_file_path


def save_subtitle(file_folder, video_title, result):
    subtitle_file_path = os.path.join(file_folder, video_title + '.srt')
    with open(subtitle_file_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments']):
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']
            f.write(f'{i + 1}\n')
            f.write(f'{format_time(start_time)} --> {format_time(end_time)}\n')
            f.write(f'{text}\n\n')
    print(f'[INFO] Subtítulos salvos em: {subtitle_file_path}')
    return subtitle_file_path
