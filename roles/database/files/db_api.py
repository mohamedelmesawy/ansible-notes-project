from flask import Flask, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

DB_PATH = "/opt/notesdb/notes.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/notes", methods=["GET"])
def get_notes():
    conn = get_connection()
    notes = conn.execute("""
        SELECT id, content, created_at
        FROM notes
        ORDER BY created_at DESC, id DESC
    """).fetchall()
    conn.close()

    return jsonify([dict(note) for note in notes])


@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return {"error": "content is required"}, 400

    conn = get_connection()
    conn.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (content,)
    )
    conn.commit()
    conn.close()

    return {"message": "note created"}, 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
    