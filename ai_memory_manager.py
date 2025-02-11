import sqlite3
import json
import os
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

# Retrieve all stored memory
def retrieve_all_memory():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation FROM memory ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows] if rows else ["No previous memory found."]

# Auto-save incoming chat messages
@app.route("/auto_save", methods=["POST"])
def auto_save():
    data = request.json
    print("Received request:", data)  # Debugging log

    user_message = data.get("user_message", "")
    solace_message = data.get("solace_message", "")

    if user_message:
        print("Saving User Message:", user_message)
        save_memory(f"User: {user_message}")
    if solace_message:
        print("Saving Solace Message:", solace_message)
        save_memory(f"Solace: {solace_message}")

    print("Returning success response")  # Debugging log
    return jsonify({"message": "Both user and Solace messages saved."})

# API Security Key (Change this to a strong key)
API_KEY = "ahuramazda32"  # Change this to any strong key you want

def authenticate(request):
    key = request.headers.get("X-API-KEY")
    return key == API_KEY

# Retrieve all stored conversations
@app.route("/retrieve", methods=["GET"])
def retrieve():
    # if not authenticate(request):  # Uncomment if you want security enabled
    #     return jsonify({"error": "Unauthorized"}), 403  
    
    all_memories = retrieve_all_memory()  
    return jsonify({"all_memories": all_memories})

# Auto-start the database and server
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)
