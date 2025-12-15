import json
import os

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

import config

OUTPUT_FILE = config.SPOTIFY_TRACKS

def fetch_saved_tracks():
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

    all_tracks = []
    results = sp.current_user_saved_tracks(limit=50)
    while results:
        for idx, item in enumerate(results['items'], 1):
            track = item['track']
            all_tracks.append({
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "album": track["album"]["name"]
            })

            if idx % config.FLUSH_INTERVAL == 0:
                os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(all_tracks, f, ensure_ascii=False, indent=2)
                print(f"Flushed {idx} tracks to {OUTPUT_FILE}")

        if results['next']:
            results = sp.next(results)
        else:
            break

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_tracks, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(all_tracks)} tracks to {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    fetch_saved_tracks()
