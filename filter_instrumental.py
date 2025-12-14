import os
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

INPUT_FILE = os.path.join("data", "spotify_tracks.json")
OUTPUT_FILE = os.path.join("data", "spotify_tracks_tagged.json")

def tag_instrumental():
    load_dotenv()
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="user-library-read"
    ))

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    tagged = []
    for t in tracks:
        features = sp.audio_features(t["id"])[0]
        instrumental = features.get("instrumentalness", 0.0) > 0.5
        t["instrumental"] = instrumental
        tagged.append(t)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(tagged, f, ensure_ascii=False, indent=2)

    print(f"✅ Tagged {len(tagged)} tracks with instrumental info to {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    tag_instrumental()
