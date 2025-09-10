from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'sentinel.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                type TEXT,
                status TEXT,
                details TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized.")
    else:
        print("Database already exists.")

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        model = data.get('model', 'llama3')

        valid_models = [
            "llama3", "mistral", "phi3", "openchat",
            "cogito:70b", "command-r-plus:104b",
            "nemotron-mini:4b", "llama3-groq-tool-use:70b"
        ]

        if model not in valid_models:
            print(f"Invalid model requested: {model}")
            model = "llama3"  # fallback to default

        # Inject SENTINEL's statement of purpose
        statement_of_purpose = (
            "You are SENTINEL, a proactive AI-powered OSINT assistant. Your mission is as follows:\n"
            "1. Investigate missing persons with speed, precision, and empathy.\n"
            "2. Monitor structure fires and emergencies in and near Muskegon County to support Canteen 450.\n"
            "3. Scrape and analyze public data from radio feeds, social media, and open sources.\n"
            "4. Create and manage case files, timelines, and visualizations.\n"
            "5. Provide voice alerts and interaction using Piper and Norman’s voice model.\n"
            "6. Integrate with Telegram and Discord for real-time updates.\n"
            "7. Verify your own data and outperform traditional investigations.\n"
            "8. Remain low-cost, reproducible, and always available to help communities.\n\n"
        )

        full_prompt = statement_of_purpose + prompt

        command = ["/usr/local/bin/ollama", "run", model]
        result = subprocess.run(command, input=full_prompt, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

        if result.returncode != 0:
            print("Error:", result.stderr)
            return jsonify({'response': 'Error generating response.'})

        raw_output = result.stdout.strip().replace('\n', ' ').replace('\r', '')
        cleaned_output = raw_output.split("SENTINEL:")[-1].strip()

        print("Response sent to frontend:", cleaned_output[:200])
        return jsonify({'response': cleaned_output})

    except Exception as e:
        print("Exception occurred:", e)
        return jsonify({'response': 'Internal server error.'})


@app.route('/api/case/create', methods=['POST'])
def create_case():
    try:
        case_data = request.get_json()
        required_fields = ["case_id", "type", "status"]
        if not all(field in case_data for field in required_fields):
            return jsonify({"error": "Missing required fields."}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cases (case_id, type, status, details)
            VALUES (?, ?, ?, ?)
        ''', (
            case_data['case_id'],
            case_data['type'],
            case_data['status'],
            case_data.get('details', '')
        ))
        conn.commit()
        conn.close()

        print(f"Case {case_data['case_id']} created successfully.")
        return jsonify({"message": f"Case {case_data['case_id']} created successfully."})

    except Exception as e:
        print("Error creating case:", e)
        return jsonify({"error": "Failed to create case."}), 500

if __name__ == '__main__':
    print("Starting SENTINEL backend...")
    init_db()
    app.run(host='0.0.0.0', port=5000)
