# Dharma Transcriptions

**Dharma Transcriptions** é um projeto completo que combina **Flask** para backend, **yt-dlp** para download de áudios do YouTube, **OpenAI Whisper** para transcrição automática e **PyTorch** para fine-tuning do modelo Whisper com dados personalizados.

O objetivo é fornecer uma solução eficiente para transcrição de áudios, geração de legendas e adaptação do modelo Whisper para domínios específicos como **vocabulario budista** e **tibetano fonético brasileiro**.

---

## 🎯 **Principais Características**

1. **Download de Áudios**: Baixe vídeos do YouTube e converta para MP3 automaticamente.
2. **Transcrição Automática**: Utilize o modelo **OpenAI Whisper** para gerar transcrições de áudio com alta precisão.
3. **Treinamento Personalizado**: Fine-tune o modelo Whisper com textos corrigidos e vocabulário específico.
4. **Geração de Legendas**: Produz arquivos de legendas no formato **SRT**.
5. **Gerenciamento de Dados**: Estrutura de pastas organizada para treinar e armazenar resultados.
6. **Interface Simples**: Backend em Flask com endpoints claros.

---

## 🚀 **Instalação**

### **Pré-requisitos**
1. **Python** (>= 3.10)
2. **Poetry** (Gerenciador de dependências)
   - Instalação: [Poetry Docs](https://python-poetry.org/docs/)
3. **FFmpeg** (para processar os áudios)
   - Verifique a instalação: `ffmpeg -version`
4. **PyTorch** (para treinamento do modelo Whisper)

---

### **Instruções de Instalação**

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/dharma-transcriptions.git
   cd dharma-transcriptions
Instale as dependências:

poetry install
Ative o ambiente virtual:

poetry shell
Configure o Flask:

set FLASK_APP=dharma_transcriptions/app.py
Inicie o servidor Flask:

flask run
Execução de Treinamento:

Baixar áudios e gerar transcrições brutas:
python -m dharma_transcriptions.training_manager
Fine-tuning do modelo Whisper:
python dharma_transcriptions/whisper_training.py
Transcrever com o modelo treinado:
python dharma_transcriptions/whisper_transcriber.py
🗂 Estrutura do Projeto
dharma-transcriptions/
├── dharma_transcriptions/
│   ├── __init__.py
│   ├── app.py                  # Inicializa o Flask
│   ├── database.py             # Gerenciamento do banco de dados SQLite
│   ├── transcription.py        # Transcrição usando Whisper
│   ├── youtube.py              # Download de áudio com yt-dlp
│   ├── utils.py                # Funções utilitárias
│   ├── whisper_training.py     # Script de treinamento (fine-tuning)
│   ├── whisper_transcriber.py  # Script para transcrever com modelo treinado
│   ├── training_manager.py     # Gerencia dados para treinamento
│   ├── downloads/              # Áudios baixados
│   ├── trained_models/         # Modelos Whisper treinados
│   │   ├── whisper_finetuned.pt
│   └── TREINAMENTO/
│       ├── audio/              # Áudios processados
│       ├── dados_brutos/       # Transcrições brutas (geradas)
│       ├── referencia_corrigida/ # Textos corrigidos usados no treinamento
│       ├── textos_corrigidos/  # Versões finais dos textos
│       └── vocabulario/        # Vocabulário budista/tibetano
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── repository.html
│   ├── view_transcription.html
├── static/
│   ├── css/
│       ├── style.css
├── tests/                      # Testes unitários
├── .gitignore
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
🛠 Como Funciona o Fluxo
Download do Áudio:
O script training_manager.py lê os links de vídeo no diretório referencia_corrigida/, baixa o áudio usando yt-dlp e salva em audio/.

Transcrição Automática:
O áudio é processado pelo modelo Whisper base, gerando transcrições brutas em dados_brutos/.

Treinamento Personalizado:
O script whisper_training.py realiza o fine-tuning do modelo Whisper, utilizando as transcrições brutas e textos corrigidos armazenados em referencia_corrigida/.

Modelo Treinado:
O modelo treinado é salvo em trained_models/whisper_finetuned.pt.

Transcrição com Modelo Personalizado:
O script whisper_transcriber.py utiliza o modelo treinado para gerar transcrições aprimoradas e legendas.

📋 Endpoints da API
GET /: Página inicial para inserção de links do YouTube.
POST /process: Processa o link do YouTube, baixa o áudio e gera transcrições.
GET /repository: Página do repositório com todas as transcrições.
GET /transcription/<id>: Visualiza a transcrição com base no ID.
🧠 Treinamento do Modelo Whisper
Para realizar o fine-tuning do modelo:

Certifique-se de ter transcrições brutas e textos corrigidos:

dados_brutos/ ➡️ Transcrições geradas pelo Whisper base.
referencia_corrigida/ ➡️ Versões corrigidas dos textos.
Execute o script de treinamento:

python dharma_transcriptions/whisper_training.py
Após o treinamento, o modelo ajustado estará salvo em:

trained_models/whisper_finetuned.pt
Para utilizar o modelo treinado:

python dharma_transcriptions/whisper_transcriber.py
❗ Erros Comuns
FFmpeg não encontrado: Certifique-se de que o FFmpeg está configurado no PATH do sistema.
Modelo não carregado: Verifique o caminho trained_models/whisper_finetuned.pt.
Dados ausentes: Certifique-se de que os diretórios dados_brutos/ e referencia_corrigida/ estão preenchidos.
🤝 Contribuição
Faça um fork do repositório.
Crie uma branch para a funcionalidade: git checkout -b minha-funcionalidade.
Faça um pull request com as suas mudanças.
📄 Licença
Este projeto está sob a MIT License.

🌟 Agradecimentos
Inspirado na necessidade de aprimorar transcrições de conteúdos budistas e tibetanos com precisão.

