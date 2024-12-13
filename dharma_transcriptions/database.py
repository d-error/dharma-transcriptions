import sqlite3

def init_db():
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def save_transcription_to_db(title, transcript_file):
    with open(transcript_file, 'r', encoding="utf-8") as file:
        content = file.read()
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("INSERT INTO transcriptions (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

def get_transcriptions():
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT id, title FROM transcriptions")
    transcriptions = c.fetchall()
    conn.close()
    return transcriptions

def get_transcription_by_id(id):
    conn = sqlite3.connect('transcriptions.db')
    c = conn.cursor()
    c.execute("SELECT title, content FROM transcriptions WHERE id=?", (id,))
    transcription = c.fetchone()
    conn.close()
    return transcription
