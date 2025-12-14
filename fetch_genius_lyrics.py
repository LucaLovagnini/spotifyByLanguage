import os
import json
import time
import requests
from dotenv import load_dotenv
from langdetect import detect_langs, DetectorFactory
from bs4 import BeautifulSoup
from collections import Counter

DetectorFactory.seed = 0

INPUT_FILE = os.path.join("data", "language_identified.json")
OUTPUT_FILE = os.path.join("data", "language_identified_genius.json")

load_dotenv()
GENIUS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
HEADERS = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
GENIUS_SEARCH_URL = "https://api.genius.com/search"

def genius_search(song_name, artist_name):
    query = f"{song_name} {artist_name}"
    params = {"q": query}
    retries = 0
    while retries < 5:
        try:
            resp = requests.get(GENIUS_SEARCH_URL, headers=HEADERS, params=params, timeout=10)
            if resp.status_code == 200:
                hits = resp.json().get("response", {}).get("hits", [])
                if not hits:
                    return {"genius_known": False, "lyrics_snippet": None}
                url = hits[0]["result"]["url"]
                lyrics = scrape_lyrics(url)
                return {"genius_known": True, "lyrics_snippet": lyrics[:400] if lyrics else None}
            elif resp.status_code == 429:
                wait = 10 * (retries + 1)
                print(f"Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
                retries += 1
            else:
                return {"genius_known": True, "lyrics_snippet": None}
        except Exception as e:
            print(f"Request error: {e}")
            time.sleep(5)
            retries += 1
    return {"genius_known": True, "lyrics_snippet": None}

def scrape_lyrics(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
        return "\n".join(div.get_text(separator="\n") for div in lyrics_divs).strip()
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def detect_language_from_lyrics(lyrics):
    try:
        langs = detect_langs(lyrics)
        top = langs[0] if langs else None
        return (top.lang, float(top.prob)) if top else ("unknown", 0.0)
    except Exception:
        return "unknown", 0.0

def augment_with_genius(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            final_tracks = {t["id"]: t for t in json.load(f)}
    else:
        final_tracks = {}

    with open(input_file, "r", encoding="utf-8") as f:
        input_tracks = json.load(f)

    for track in input_tracks:
        if track["id"] in final_tracks:
            continue

        if track.get("final_language") != "unknown":
            track.update({
                "source": "metadata",
                "genius_known": None,
                "lyrics_snippet": None
            })
            final_tracks[track["id"]] = track
            continue

        print(f"Fetching Genius data for: {track['name']} - {track['artist']}")
        genius_result = genius_search(track["name"], track["artist"])
        if genius_result["lyrics_snippet"]:
            lang, conf = detect_language_from_lyrics(genius_result["lyrics_snippet"])
        else:
            lang, conf = "unknown", 0.0

        track.update({
            "final_language": lang,
            "confidence": round(conf, 4),
            "source": "genius" if genius_result["genius_known"] else "genius_not_found",
            "genius_known": genius_result["genius_known"],
            "lyrics_snippet": genius_result["lyrics_snippet"]
        })
        final_tracks[track["id"]] = track
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(list(final_tracks.values()), f, ensure_ascii=False, indent=2)
        time.sleep(1)

    counts = Counter(t["final_language"] for t in final_tracks.values())
    print("=== Genius Language Summary ===")
    for lang, cnt in counts.most_common():
        print(f"{lang}: {cnt}")
    print(f"✅ Saved {len(final_tracks)} tracks with Genius data to {output_file}")
    return output_file

if __name__ == "__main__":
    augment_with_genius()
