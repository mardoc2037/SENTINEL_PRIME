from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

llama_bin = "/home/mardoc2037/llama.cpp/build/bin/llama-cli"
model_path = "/home/mardoc2037/models/llama-7b.Q4_K_M.gguf"

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        print(f"Received prompt: {prompt}")

        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        result = subprocess.run(
        [llama_bin, "-m", model_path, "-p", prompt, "--n-predict", "128"],
        capture_output=True,
        text=True,
        timeout=60
)


        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        return jsonify({'response': result.stdout.strip()})
    except Exception as e:
        print("Exception:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
