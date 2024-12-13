from flask import render_template, jsonify, request  # Certifique-se de importar render_template
from dharma_transcriptions.database import save_transcription_to_db, get_transcriptions, get_transcription_by_id
from dharma_transcriptions.youtube import download_audio
from dharma_transcriptions.transcription import transcribe_audio_and_generate_subtitles
from dharma_transcriptions.utils import sanitize_filename

def register_routes(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/repository")
    def repository():
        transcriptions = get_transcriptions()
        return render_template("repository.html", transcriptions=transcriptions)

    @app.route("/transcription/<int:id>")
    def view_transcription(id):
        transcription = get_transcription_by_id(id)
        if transcription:
            return render_template("view_transcription.html", title=transcription[0], content=transcription[1])
        else:
            return jsonify({"success": False, "error": "Transcrição não encontrada."}), 404

    @app.route("/process", methods=["POST"])
    def process_youtube():
        data = request.get_json()
        youtube_url = data.get("youtube_url")
        if not youtube_url:
            return jsonify({"success": False, "error": "URL do YouTube não fornecida."})

        try:
            print("[INFO] Iniciando download do áudio...")
            output_file, video_title = download_audio(youtube_url)
            print(f"[INFO] Áudio baixado: {output_file}")

            print("[INFO] Iniciando transcrição...")
            transcript_file, subtitle_file = transcribe_audio_and_generate_subtitles(output_file, video_title)
            print(f"[INFO] Transcrição concluída: {transcript_file}")
            print(f"[INFO] Subtítulos gerados: {subtitle_file}")

            print("[INFO] Salvando transcrição no banco de dados...")
            save_transcription_to_db(video_title, transcript_file)
            print("[INFO] Transcrição salva no banco de dados.")

            return jsonify({
                "success": True,
                "audio_file": f"/download/audio/{sanitize_filename(video_title)}",
                "transcript_file": f"/download/transcription/{sanitize_filename(video_title)}",
                "subtitle_file": f"/download/subtitles/{sanitize_filename(video_title)}"
            })
        except Exception as e:
            print(f"[ERROR] Erro ao processar o vídeo: {str(e)}")
            return jsonify({"success": False, "error": str(e)})
