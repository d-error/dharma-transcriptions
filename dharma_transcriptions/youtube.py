import os

import yt_dlp

from dharma_transcriptions.config import Config
from dharma_transcriptions.utils import sanitize_filename


def download_audio(youtube_url):
    output_folder = Config.OUTPUT_FOLDER
    os.makedirs(output_folder, exist_ok=True)
    ffmpeg_location = Config.FFMPEG_LOCATION

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(
            output_folder, sanitize_filename('%(title)s'), '%(title)s.%(ext)s'
        ),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
        ],
        'ffmpeg_location': ffmpeg_location,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                youtube_url, download=True
            )  # TODO: tem uma opção -o no yt-dlp
            # pra definir template do download

            raw_title = info_dict.get('title', 'arquivo_desconhecido')
            sanitized_title = sanitize_filename(raw_title)
            output_folder = os.path.join(output_folder, sanitized_title)
            audio_file = os.path.join(output_folder, f'{sanitized_title}.mp3')

            # Renomeie o arquivo após o download e sanitização
            downloaded_file = ydl.prepare_filename(info_dict)
            downloaded_file = os.path.splitext(downloaded_file)[0] + '.mp3'

            os.rename(downloaded_file, audio_file)
            return (
                audio_file,
                sanitized_title,
            )  # Retorna apenas o caminho do arquivo
    except Exception as e:
        raise Exception(f'Erro ao baixar ou converter áudio: {str(e)}') from e
