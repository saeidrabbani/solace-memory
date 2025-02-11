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

@app.route("/auto_save", methods=["POST"])
def auto_save():
    data = request.json
    print("Received request:", data)  # Print incoming request data

    user_message = data.get("user_message", "")
    solace_message = data.get("solace_message", "")

    if user_message:
        print("Saving User Message:", user_message)
        save_memory(f"User: {user_message}")
    if solace_message:
        print("Saving Solace Message:", solace_message)
        save_memory(f"Solace: {solace_message}")

    print("Returning success response")  # Debug message
    return jsonify({"message": "Both user and Solace messages saved."})


API_KEY = "ahuramazda32"  # Change this to any strong key you want

def authenticate(request):
    key = request.headers.get("X-API-KEY")
    return key == API_KEY

@app.route("/retrieve", methods=["GET"])
def retrieve():
   #  if not authenticate(request):
    #     return jsonify({"error": "Unauthorized"}), 403  # Reject requests without the correct API key
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT conversation FROM memory ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()
    
    all_memories = [row[0] for row in rows]  # Convert DB rows to a list of memories
    
    return jsonify({"all_memories": all_memories})



if __name__ == "__main__":
    init_db()
    app.run(port=5000)
