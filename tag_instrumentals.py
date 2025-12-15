import json
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

import config

# -----------------------------
# Spotify Setup
# -----------------------------
load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "user-library-read"


def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))


# -----------------------------
# Config
# -----------------------------
INPUT_FILE = os.path.join("data", "spotify_tracks.json")
OUTPUT_FILE = os.path.join("data", "spotify_tracks_tagged.json")


# -----------------------------
# Main Logic
# -----------------------------
def tag_instrumentals(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    sp = get_spotify_client()

    with open(input_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    skipped_tracks = []

    for track in tracks:
        try:
            features = sp.audio_features([track["id"]])[0]
            if features is None:
                raise Exception("Audio features not available")
            track["instrumentalness"] = features.get("instrumentalness", 0.0)
            track["is_instrumental"] = track["instrumentalness"] >= config.INSTRUMENTAL_THRESHOLD
        except Exception as e:
            print(f"⚠️ Skipping track {track['id']}: {e}")
            track["instrumentalness"] = 0.0
            track["is_instrumental"] = False
            skipped_tracks.append(track["id"])

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(tracks, f, ensure_ascii=False, indent=2)

    total_inst = sum(t["is_instrumental"] for t in tracks)
    print(f"✅ Tagged {len(tracks)} tracks, {total_inst} are instrumental.")
    if skipped_tracks:
        print(f"⚠️ {len(skipped_tracks)} tracks were skipped due to missing features. IDs saved to log file.")

    # Optional: save skipped track IDs to a log file
    log_file = os.path.join("data", "skipped_instrumental_tracks.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(skipped_tracks, f, ensure_ascii=False, indent=2)

    print(f"Output saved to {output_file}, skipped tracks log saved to {log_file}")
    return output_file  # for orchestrator usage


# -----------------------------
# CLI / Standalone Run
# -----------------------------
if __name__ == "__main__":
    tag_instrumentals()
