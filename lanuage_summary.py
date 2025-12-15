import json
import sys
from collections import Counter

import pycountry


def code_to_language(lang_code):
    """Convert ISO 639-1 code to full language name, fallback to code if unknown."""
    if not lang_code or lang_code == "unknown":
        return "Unknown"
    try:
        return pycountry.languages.get(alpha_2=lang_code).name
    except Exception:
        return lang_code  # fallback if not found

def extract_language(track):
    if "final_language" in track:
        return track["final_language"]
    return track.get("language", "unknown")

def summarize_languages(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    summary = Counter()
    total = 0

    for track in tracks:
        lang = extract_language(track)
        summary[lang] += 1
        total += 1

    print("=== Language Summary ===")
    for lang, count in summary.most_common():
        pct = (count / total) * 100
        lang_name = code_to_language(lang)
        print(f"{lang:5s} {lang_name:20s} {count:5d} ({pct:5.2f}%)")
    print(f"\nTotal tracks: {total}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python language_summary.py <input_file.json>")
        sys.exit(1)

    summarize_languages(sys.argv[1])
