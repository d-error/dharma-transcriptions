import os

import yt_dlp

from dharma_transcriptions.config import Config
from yt_dlp.utils import sanitize_filename


def download_audio(youtube_url):
    output_folder = Config.OUTPUT_FOLDER
    os.makedirs(output_folder, exist_ok=True)
    ffmpeg_location = Config.FFMPEG_LOCATION
    ydl_opts = {
        'format': 'bestaudio/best',
        
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
        ],
        'ffmpeg_location': ffmpeg_location
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(
                youtube_url, download=True
            )  # TODO: tem uma opção -o no yt-dlp
            # pra definir template do download

            raw_title = info_dict.get('title', 'video')
            sanitized_title = sanitize_filename(raw_title.lower()).replace(' ', '_')
            outtmpl_filepath = os.path.join(output_folder, sanitized_title, f'{sanitized_title}.%(ext)s')
            ydl_opts['outtmpl'] = outtmpl_filepath
            audio_file = outtmpl_filepath.replace("%(ext)s", 'mp3')
        
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            

            return (
                audio_file,
                sanitized_title,
            )  # Retorna apenas o caminho do arquivo """
    except Exception as e:
        raise Exception(f'Erro ao baixar ou converter áudio: {str(e)}') from e
