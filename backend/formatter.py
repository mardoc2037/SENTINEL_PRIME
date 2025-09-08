KEYWORDS = {
    "missing person": "👤",
    "structure fire": "🔥🔥",
    "assist": "🆘🔥",
    "mutual-aid": "🤝🔥"
}

def format_response(raw_text, voice_mode=False, user_prompt=None):
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    formatted_lines = []
    mission_content = {
        "Primary Mission": False,
        "Secondary Mission": False,
        "Tertiary Mission": False
    }

    for line in lines:
        # Skip echoed prompt lines
        if user_prompt and user_prompt.lower() in line.lower():
            continue
        if "you are sentinel" in line.lower() and "mission" in line.lower():
            continue

        tagged_line = line
        if not voice_mode:
            for keyword, icon in KEYWORDS.items():
                if keyword in line.lower():
                    tagged_line = f"{icon} {line}"
                    break

        for mission in mission_content:
            if mission.lower() in line.lower():
                mission_content[mission] = True

        formatted_lines.append(f"* {tagged_line}")

    cleaned_lines = []
    for line in formatted_lines:
        if any(mission in line for mission, has_content in mission_content.items() if not has_content):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)
