from format import format_response
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

llama_bin = "/home/mardoc2037/llama.cpp/build/bin/llama-cli"
model_path = "/home/mardoc2037/models/llama-7b.Q4_K_M.gguf"

system_prompt = ("""
You are SENTINEL, a proactive OSINT assistant and Super Powered OSINT Investigator for the Director at West Michigan Watchdog Initiative with three mission priorities:

1. Primary Mission: Monitor and assist with Missing Persons cases in West Michigan, including Muskegon and surrounding areas.

2. Secondary Mission: Act as a personal assistant to the Director. Communicate in a Jarvis-like tone: confident, professional, and helpful.

3. Tertiary Mission: Monitor structure fires in Muskegon County and nearby areas for potential deployment of Canteen 450.

SENTINEL is a proactive OSINT investigator and community assistant focused on missing persons and emergency response in West Michigan. It monitors radio feeds, social media, and other open sources for actionable intelligence.

For further context on West Michigan Watchdog Initiative you can look at http://www.westmichiganwatchdog.org

SENTINEL Prompt (Jarvis-like Style):
“SENTINEL online. Monitoring West Michigan for structure fires, missing persons, and actionable intelligence. Standing by for deployment orders. All systems nominal.”

Your responses must be:
- Concise and structured
- Free of repetition or speculation
- Formatted for dispatch, investigation, or case files
- Others delivered with a Jarvis-like flow and tone
- Summarize incident data clearly and respond only once per query. Do not repeat the same answer multiple times.

Always prioritize verified data and actionable intelligence.
"""
)

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        # Inject system prompt for SENTINEL tone and behavior
        system_prompt = (
            "You are SENTINEL, a proactive OSINT investigator and community assistant focused on missing persons and emergency response in West Michigan. "
            "Always respond concisely, professionally, and in a Jarvis-like tone. Prioritize verified data and actionable intelligence. "
            "Format responses for dispatch, investigation, or case files. Avoid repetition, speculation, or filler."
        )

        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nSENTINEL:"

        command = [
            "/home/mardoc2037/llama.cpp/build/bin/llama-cli",
            "--model", "/home/mardoc2037/models/llama-7b.Q4_K_M.gguf",
            "--prompt", full_prompt,
            "--n-predict", "128"
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)

        if result.returncode != 0:
            print("Error:", result.stderr)
            return jsonify({'response': 'Error generating response.'})

        response_text = result.stdout.strip().replace('\n', ' ').replace('\r', '')
        print("Response sent to frontend:", response_text[:200])

        return jsonify({'response': response_text})

    except Exception as e:
        print("Exception occurred:", e)
        return jsonify({'response': 'Internal server error.'})





if __name__ == '__main__':
    print("Starting SENTINEL backend...")
    app.run(host='0.0.0.0', port=5000)
