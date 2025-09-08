def format_response(raw_output, voice_mode=False, user_prompt=""):
    # Basic cleanup: remove repeated lines and trim whitespace
    lines = raw_output.strip().split('\n')
    seen = set()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if line and line not in seen:
            cleaned_lines.append(line)
            seen.add(line)

    response = "\n".join(cleaned_lines)

    # Optional: add voice formatting
    if voice_mode:
        response = f"[Voice Mode Enabled]\n{response}"

    return response
