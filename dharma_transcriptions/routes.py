from flask import (
    jsonify,
    render_template,
    request,
)

from dharma_transcriptions.database import (
    get_transcription_by_id,
    get_transcriptions,
    save_transcription_to_db,
)
from dharma_transcriptions.transcription import (
    transcribe_audio_and_generate_subtitles,
)
from dharma_transcriptions.utils import sanitize_filename
from dharma_transcriptions.youtube import download_audio


def register_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/repository')
    def repository():
        transcriptions = get_transcriptions()
        return render_template(
            'repository.html', transcriptions=transcriptions
        )

    @app.route('/transcription/<int:id>')
    def view_transcription(id):
        transcription = get_transcription_by_id(id)
        if transcription:
            return render_template(
                'view_transcription.html',
                title=transcription[0],
                content=transcription[1],
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Transcrição não encontrada.',
            }), 404

    @app.route('/process', methods=['POST'])
    def process_youtube():
        data = request.get_json()
        youtube_url = data.get('youtube_url')
        if not youtube_url:
            return jsonify({
                'success': False,
                'error': 'URL do YouTube não fornecida.',
            })

        try:
            print('[INFO] Iniciando download do áudio...')
            audio_file, file_title, file_folder = download_audio(youtube_url)
            print(f'[INFO] Áudio baixado: {audio_file}')

            print('[INFO] Iniciando transcrição...')
            transcript_file, subtitle_file = (
                transcribe_audio_and_generate_subtitles(
                    audio_file, file_title, file_folder
                )
            )
            print(f'[INFO] Transcrição concluída: {transcript_file}')
            print(f'[INFO] Subtítulos gerados: {subtitle_file}')

            print('[INFO] Salvando transcrição no banco de dados...')
            save_transcription_to_db(file_title, transcript_file)
            print('[INFO] Transcrição salva no banco de dados.')

            return jsonify({
                'success': True,
                'audio_file': audio_file,
                'transcript_file': transcript_file,
                'subtitle_file': subtitle_file,
            })

        except Exception as e:
            print(f'[ERROR] Erro ao processar o vídeo: {str(e)}')
            return jsonify({'success': False, 'error': str(e)})
