import subprocess
import requests
import os
import logging

# -------------------- GGUF Model Paths --------------------
LLAMA_CPP_MODELS = {
    "phi-3-mini-4k-instruct": "/home/mardoc2037/llama.cpp/models/Phi-3-mini-4k-instruct-q4.gguf",
    "cogito-v1-preview-llama-70B": "/home/mardoc2037/llama.cpp/models/cogito-v1-preview-llama-70B-Q4_K_M.gguf",
    "llama-3-groq-70B-tool-use": "/home/mardoc2037/llama.cpp/models/Llama-3-Groq-70B-Tool-Use-Q4_K_M.gguf",
    "openchat-3.5-1210": "/home/mardoc2037/llama.cpp/models/openchat-3.5-1210.Q4_K_M.gguf",
    "codellama-7b-instruct": "/home/mardoc2037/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf",
    "mistral-7b-instruct-v0.2": "/home/mardoc2037/llama.cpp/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
    "mistral-nemo-prism-12B": "/home/mardoc2037/llama.cpp/models/Mistral-Nemo-Prism-12B-Q4_K_M.gguf",
    "llama-7b": "/home/mardoc2037/llama.cpp/models/llama-7b.Q4_K_M.gguf"
}

# -------------------- Model Execution --------------------
def run_model(model_name, prompt):
    if model_name in LLAMA_CPP_MODELS:
        model_path = LLAMA_CPP_MODELS[model_name]
        try:
            result = subprocess.run(
                [
                    "./main",  # Adjust if your llama.cpp binary is named differently
                    "-m", model_path,
                    "-p", prompt,
                    "--temp", "0.7",
                    "--n-predict", "256"
                ],
                cwd="/home/mardoc2037/llama.cpp",
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logging.error(f"llama.cpp error: {result.stderr}")
                return f"Error running llama.cpp model: {result.stderr}"
            return result.stdout.strip()
        except Exception as e:
            logging.exception("llama.cpp execution failed")
            return f"Exception during llama.cpp execution: {str(e)}"

    # -------------------- Ollama Execution --------------------
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            headers={"Content-Type": "application/json"},
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        logging.exception("Ollama execution failed")
        return f"Error running Ollama model: {str(e)}"
