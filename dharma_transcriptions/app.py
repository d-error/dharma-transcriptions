import os
import re
import sqlite3
from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import whisper

app = Flask(_name_)

# Função para sanitizar nomes de arquivos e pastas
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Banco de dados SQLite
def init_db():
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Página inicial
@app.route("/")
def home():
    return render_template("index.html")

# Página de repositório
@app.route("/repository")
def repository():
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT id, title FROM transcriptions")
    transcriptions = c.fetchall()
    conn.close()
    return render_template("repository.html", transcriptions=transcriptions)

# Visualizar uma transcrição
@app.route("/transcription/<int:id>")
def view_transcription(id):
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT title, content FROM transcriptions WHERE id=?", (id,))
    transcription = c.fetchone()
    conn.close()
    if transcription:
        return render_template("view_transcription.html", title=transcription[0], content=transcription[1])
    else:
        return jsonify({"success": False, "error": "Transcrição não encontrada."}), 404

# Processar link do YouTube
@app.route("/process", methods=["POST"])
def process_youtube():
    data = request.get_json()
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return jsonify({"success": False, "error": "URL do YouTube não fornecida."})

    try:
        # Baixar áudio do YouTube
        output_file, video_title = download_audio(youtube_url)
        # Transcrever áudio e gerar legendas
        transcript_file, subtitle_file = transcribe_audio_and_generate_subtitles(output_file, video_title)
        # Salvar no banco de dados
        save_transcription_to_db(video_title, transcript_file)
        # Retornar arquivos para o frontend
        return jsonify({
            "success": True,
            "audio_file": f"/download/audio/{sanitize_filename(video_title)}",
            "transcript_file": f"/download/transcription/{sanitize_filename(video_title)}",
            "subtitle_file": f"/download/subtitles/{sanitize_filename(video_title)}"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Função para baixar áudio do YouTube
def download_audio(youtube_url):
    output_folder = "downloads"
    os.makedirs(output_folder, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"},
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            raw_title = info_dict.get("title", "arquivo_desconhecido")
            sanitized_title = sanitize_filename(raw_title)
            video_folder = os.path.join(output_folder, sanitized_title)
            os.makedirs(video_folder, exist_ok=True)
            audio_file = os.path.join(video_folder, "audio.mp3")
            os.rename(ydl.prepare_filename(info_dict).replace(".webm", ".mp3"), audio_file)
            return audio_file, sanitized_title
    except Exception as e:
        raise Exception(f"Erro ao baixar ou converter áudio: {str(e)}")

# Função para transcrever áudio e gerar legendas
def transcribe_audio_and_generate_subtitles(audio_file, video_title):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    transcript_folder = os.path.join("downloads", video_title)
    os.makedirs(transcript_folder, exist_ok=True)

    # Salvar transcrição
    transcript_file_path = os.path.join(transcript_folder, "transcription.txt")
    with open(transcript_file_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Salvar legendas
    subtitle_file_path = os.path.join(transcript_folder, "subtitles.srt")
    with open(subtitle_file_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result["segments"]):
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            f.write(f"{i + 1}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
    return transcript_file_path, subtitle_file_path

# Função para formatar tempo
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Salvar transcrição no banco de dados
def save_transcription_to_db(title, transcript_file):
    with open(transcript_file, 'r', encoding="utf-8") as file:
        content = file.read()
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("INSERT INTO transcriptions (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

# Inicializar banco e rodar servidor
if _name_ == "_main_":
    init_db()
    app.run(host="0.0.0.0", port=5000)
