import subprocess
import requests
import logging

LLAMA_BINARY = "/home/mardoc2037/llama.cpp/build/bin/llama-cli"  # Adjust if needed

def run_llama_cpp(model_path, prompt, n_predict=200, temperature=0.7):
    command = [
        LLAMA_BINARY,
        "-m", model_path,
        "-p", prompt,
        "--n-predict", str(n_predict),
        "--temp", str(temperature)
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            logging.error(f"llama.cpp failed: {result.stderr}")
            return "Error: llama.cpp execution failed."
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Exception during llama.cpp execution: {e}")
        return "Error: Exception during llama.cpp execution."

def run_ollama(model_name, prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": prompt}
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "Error: No response from Ollama.")
    except Exception as e:
        logging.error(f"Ollama execution failed: {e}")
        return "Error: Ollama execution failed."

def run_model(model_name, model_path, prompt):
    if model_name in ["phi-3", "mistral", "openchat", "llama3", "gpt3", "openai-gpt2-xl"]:
        return run_ollama(model_name, prompt)
    else:
        return run_llama_cpp(model_path, prompt)
