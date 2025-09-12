def choose_model(prompt, available_models):
    length = len(prompt.split())
    prompt_lower = prompt.lower()

    # Keyword-based routing (optional)
    if "legal" in prompt_lower and "openchat" in available_models:
        return "openchat"
    if "creative" in prompt_lower and "mistral" in available_models:
        return "mistral"

    # Length-based routing
    if length < 50 and "phi-3" in available_models:
        return "phi-3"
    elif length < 150 and "mistral" in available_models:
        return "mistral"
    elif "llama" in available_models:
        return "llama"

    # Fallback
    return list(available_models.keys())[0]
