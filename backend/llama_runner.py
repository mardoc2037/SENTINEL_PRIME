import subprocess

LLAMA_BINARY = "/home/mardoc2037/llama.cpp/build/bin/llama-cli"
MODEL_PATH = "/home/mardoc2037/llama.cpp/models/codellama-7b-instruct.Q4_K_M.gguf"

def run_llama(prompt):
    try:
        result = subprocess.run(
            [LLAMA_BINARY, "-m", MODEL_PATH, "-p", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
