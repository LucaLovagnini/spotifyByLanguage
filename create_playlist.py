import json
import os
import sys
import time

import spotipy
from dotenv import load_dotenv
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth

import config

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = "playlist-modify-public playlist-modify-private"

# -----------------------------
# Spotify Client
# -----------------------------
def get_spotify_client():
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=config.SPOTIFY_PLAYLIST_SCOPE
    ))

# -----------------------------
# Helpers
# -----------------------------
def chunked(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]

# -----------------------------
# Create Playlist for One Language
# -----------------------------
def create_playlist(input_file, language, min_songs=10, sp=None, max_retries=5):
    with open(input_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    # collect tracks of this language
    lang_tracks = [t["id"] for t in tracks if t.get("final_language") == language]

    if sp is None:
        sp = get_spotify_client()

    total_tracks = len(lang_tracks)
    if total_tracks < min_songs:
        print(f"⚠️ Skipping {language}: only {total_tracks} tracks (need at least {min_songs})")
        return

    user_id = sp.me()["id"]
    playlist_name = f"My {language.upper()} Songs"

    attempt = 0
    while attempt < max_retries:
        try:
            print(f"\n🎶 Creating playlist '{playlist_name}' with {total_tracks} tracks...")
            playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
            time.sleep(1)

            for idx, batch in enumerate(chunked(lang_tracks, 100), start=1):
                sp.playlist_add_items(playlist["id"], batch)
                print(f"   → Added {min(idx*100, total_tracks)}/{total_tracks} tracks...")
                time.sleep(1)

            print(f"✅ Finished playlist '{playlist_name}' with {total_tracks} tracks.")
            return
        except SpotifyException as e:
            if e.http_status == 429:
                retry_after = int(e.headers.get("Retry-After", "5"))
                print(f"⏱ Rate limited, waiting {retry_after}s...")
                time.sleep(retry_after)
            elif 500 <= e.http_status < 600:
                print(f"⚠️ Server error {e.http_status}, retrying in 2s...")
                time.sleep(2)
            else:
                raise e
        except Exception as ex:
            print(f"⚠️ Unexpected error: {ex}, retrying in 2s...")
            time.sleep(2)
        attempt += 1

    print(f"❌ Failed to create playlist '{playlist_name}' after {max_retries} attempts.")

# -----------------------------
# Create Playlists for Many Languages
# -----------------------------
def create_playlists_from_file(input_file, languages, min_songs=10, sp=None):
    if sp is None:
        sp = get_spotify_client()

    for lang in languages:
        create_playlist(input_file, lang, min_songs=min_songs, sp=sp)

# -----------------------------
# CLI
# -----------------------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python create_playlist.py <tracks_file.json> <lang1,lang2,...> [min_songs]")
        sys.exit(1)

    input_file = sys.argv[1]
    languages = sys.argv[2].split(",")
    min_songs = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    sp = get_spotify_client()
    create_playlists_from_file(input_file, languages, min_songs, sp=sp)

if __name__ == "__main__":
    main()
