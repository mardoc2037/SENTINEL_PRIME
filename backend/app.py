from datetime import datetime
from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from flask_socketio import SocketIO

import subprocess
import os
import uuid
import sqlite3
import logging
import requests

from model_runner import run_model  # ✅ Unified model execution

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    filename='sentinel_backend.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# -------------------- DATABASE INIT --------------------
def init_db():
    conn = sqlite3.connect('sentinel.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            location TEXT,
            details TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            model TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# -------------------- MODEL DETECTION --------------------

def detect_models():
    search_dirs = [
        "/home/mardoc2037/llama.cpp/",
        "/home/mardoc2037/llama.cpp/models/"
    ]
    model_paths = {}
    max_files = 50

    try:
        for model_dir in search_dirs:
            count = 0
            for root, dirs, files in os.walk(model_dir):
                for file in files:
                    if count >= max_files:
                        break
                    if (
                        file.endswith(".gguf") and
                        "vocab" not in file.lower() and
                        "tokenizer" not in file.lower() and
                        "config" not in file.lower()
                    ):
                        full_path = os.path.join(root, file)
                        if os.path.getsize(full_path) > 100 * 1024 * 1024:
                            key = os.path.splitext(file)[0].lower()
                            model_paths[key] = full_path
                            count += 1
    except Exception as e:
        logging.error(f"Model detection failed: {e}")

    return model_paths


# -------------------- LOGGING SETUP --------------------
logging.basicConfig(
    filename='sentinel_backend.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# -------------------- DATABASE INIT --------------------
def init_db():
    conn = sqlite3.connect('sentinel.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            location TEXT,
            details TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_stats (
            model TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# -------------------- MODEL DETECTION --------------------
#def detect_models():
#    search_dirs = [
#        "/home/mardoc2037/llama.cpp/",
#        "/home/mardoc2037/llama.cpp/models/"
#    ]
#    model_paths = {}
#    max_files = 50
#
#    try:
#        for model_dir in search_dirs:
#            count = 0
#            for root, dirs, files in os.walk(model_dir):
#                for file in files:
#                    if count >= max_files:
#                        break
#                    if (
#                        file.endswith(".gguf") and
#                        "vocab" not in file.lower() and
#                        "tokenizer" not in file.lower() and
#                        "config" not in file.lower()
#                    ):
#                        full_path = os.path.join(root, file)
#                        try:
#                            if os.path.getsize(full_path) > 100 * 1024 * 1024:
#                                key = os.path.splitext(file)[0].lower()
#                                model_paths[key] = full_path
#                                count += 1
#                        except Exception as size_error:
#                            logging.warning(f"Skipping file due to size check error: {full_path} - {size_error}")
#        logging.info(f"Detected {len(model_paths)} models.")
#    except Exception as e:
#        logging.error(f"Model detection failed: {e}")
#
#    return model_paths
#
#MODEL_PATHS = detect_models()
#logging.info(f"Loaded models: {list(MODEL_PATHS.keys())}")

# -------------------- USAGE TRACKING --------------------
def increment_usage(model_key):
    try:
        conn = sqlite3.connect('sentinel.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usage_stats (model, count)
            VALUES (?, 1)
            ON CONFLICT(model) DO UPDATE SET count = count + 1
        ''', (model_key,))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Failed to update usage stats for {model_key}: {e}")

# -------------------- ROUTE: LIST MODELS --------------------
@app.route('/models', methods=['GET'])
def get_models():
    models = list(LLAMA_CPP_MODELS.keys())  # from model_runner.py

    try:
        res = requests.get("http://localhost:11434/api/tags")
        if res.ok:
            ollama_models = [m["name"] for m in res.json().get("models", [])]
            models.extend(ollama_models)
    except Exception as e:
        logging.warning(f"Failed to fetch Ollama models: {str(e)}")

    return jsonify({"models": sorted(models)})


# -------------------- ROUTE: CASE CREATION --------------------
@app.route('/create_case', methods=['POST'])
def create_case():
    try:
        case_data = request.json
        conn = sqlite3.connect('sentinel.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cases (case_id, name, age, location, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            case_data['case_id'],
            case_data.get('name', ''),
            case_data.get('age', 0),
            case_data.get('location', ''),
            case_data.get('details', '')
        ))
        conn.commit()
        conn.close()

        logging.info(f"Case created: {case_data['case_id']}")
        return jsonify({"message": f"Case {case_data['case_id']} created successfully."})

    except Exception as e:
        logging.error(f"Error creating case: {e}")
        return jsonify({"error": "Failed to create case."}), 500

# -------------------- ROUTE: PIPER SPEECH --------------------

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '')
    if not text:
        return {"error": "No text provided"}, 400

    model_path = "/home/mardoc2037/piper/models/jarvis-medium.onnx"
    output_path = "/tmp/piper_output.wav"

    try:
        subprocess.run([
            "/home/mardoc2037/piper/piper_binary/piper",
            "--model", model_path,
            "--output_file", output_path,
            "--text", text
        ], check=True)
    except subprocess.CalledProcessError as e:
        return {"error": "Piper failed to generate audio", "details": str(e)}, 500

    if os.path.exists(output_path):
        return send_file(output_path, mimetype="audio/wav")
    else:
        return {"error": "Audio file not found"}, 500



# -------------------- MODEL MAP + ADAPTIVE LOGIC --------------------

MODEL_MAP = {
    "llama3": "llama3.1:405b",
    "phi4": "phi4-mini:3.8b",
    "nemotron": "nemotron-mini:4b",
    "commandr": "command-r-plus:104b",
    "deepseek": "deepseek-v3.1:671b"
}

def select_model(prompt):
    prompt_lower = prompt.lower()

    if any(keyword in prompt_lower for keyword in ["math", "calculate", "equation", "solve"]):
        return MODEL_MAP["phi4"]
    elif any(keyword in prompt_lower for keyword in ["code", "python", "javascript", "function"]):
        return MODEL_MAP["commandr"]
    elif any(keyword in prompt_lower for keyword in ["search", "intel", "osint", "investigate"]):
        return MODEL_MAP["deepseek"]
    elif any(keyword in prompt_lower for keyword in ["summarize", "explain", "write", "email"]):
        return MODEL_MAP["llama3"]
    else:
        return MODEL_MAP["nemotron"]  # fallback if no match

# -------------------- ROUTE: GENERATE --------------------

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    model_key = data.get("model", "adaptive")
    prompt = data.get("prompt", "")

    if model_key == "adaptive":
        model = select_model(prompt)
    else:
        model = MODEL_MAP.get(model_key, MODEL_MAP["llama3"])

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        response.raise_for_status()
        result = response.json()
        return jsonify({"response": result.get("response", "No response received.")})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error running Ollama model: {str(e)}"}), 500

# -------------------- START APP --------------------

if __name__ == '__main__':
    logging.info("Starting SENTINEL backend...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
