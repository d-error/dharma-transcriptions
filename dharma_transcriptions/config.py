import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_PATH = os.getenv('BASE_PATH', default=__file__)
    OUTPUT_FOLDER = os.getenv(
        'OUTPUT_FOLDER', default=os.path.join('output')
    )
    WHISPER_MODEL = os.getenv('WHISPER_MODEL', default='base')
    FFMPEG_LOCATION = os.getenv('FFMPEG_LOCATION')
