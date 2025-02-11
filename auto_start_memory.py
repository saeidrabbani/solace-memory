from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

MEMORY_URL = "https://solace-memory.onrender.com/retrieve"

def fetch_memory():
    try:
        response = requests.get(MEMORY_URL)
        if response.status_code == 200:
            data = response.json()
            return data["all_memories"]
        else:
            return ["❌ Failed to retrieve memory."]
    except Exception as e:
        return [f"⚠️ Error fetching memory: {e}"]

@app.route("/auto-retrieve", methods=["GET"])
def auto_retrieve():
    memory = fetch_memory()
    return jsonify({"retrieved_memory": memory})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)
