import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")
    WHISPER_MODEL = os.getenv("WHISPER_MODEL", default='base')