import sqlite3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

db_file = "solace_memory.db"

# Create database to store memory if it doesn't exist
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            conversation TEXT
        )
    """)
    conn.commit()
    conn.close()

# Save conversation to memory
def save_memory(conversation):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO memory (conversation) VALUES (?)", (conversation,))
    conn.commit()
    conn.close()

# Retrieve last memory entry
def retrieve_last_memory():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation FROM memory ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "No previous memory found."

@app.route("/save", methods=["POST"])
def save():
    data = request.json
    conversation = data.get("conversation", "")
    save_memory(conversation)
    return jsonify({"message": "Memory saved."})

@app.route("/retrieve", methods=["GET"])
def retrieve():
    memory = retrieve_last_memory()
    return jsonify({"last_memory": memory})

if __name__ == "__main__":
    init_db()
    app.run(port=5000)
