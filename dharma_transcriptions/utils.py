import re


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?* ]', '_', filename)


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = round((seconds % 1) * 1000)
    return f'{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}'
