import os

import yt_dlp
from dharma_transcriptions.utils import sanitize_filename

from dharma_transcriptions.config import Config


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

            sanitized_title = get_sanitized_title(info_dict)
            outtmpl_filepath = get_outtmpl_filepath(
                sanitized_title, output_folder
            )
            file_folder = os.path.join(output_folder, sanitized_title)
            audio_file = outtmpl_filepath.replace('%(ext)s', 'mp3')

            ydl_opts['outtmpl'] = outtmpl_filepath

            with yt_dlp.YoutubeDL(ydl_opts) as ydl_sanitized_path:
                ydl_sanitized_path.download([youtube_url])

            #TODO upload to s3?
            absolute_audio_file_path = os.path.abspath(audio_file)
            absolute_folder_path = os.path.abspath(file_folder)

            return (absolute_audio_file_path, sanitized_title, absolute_folder_path)
    except Exception as e:
        raise Exception(f'Erro ao baixar ou converter áudio: {str(e)}') from e


def get_sanitized_title(info_dict):
    raw_title = info_dict.get('title', 'video')
    return sanitize_filename(raw_title)


def get_outtmpl_filepath(sanitized_title, output_folder):
    outtmpl_filepath = os.path.join(
        output_folder, sanitized_title, f'{sanitized_title}.%(ext)s'
    )
    return outtmpl_filepath
