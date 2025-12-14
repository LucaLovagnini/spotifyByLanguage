import sys

from create_playlist import create_playlists_from_file
from detect_language import detect_languages
from fetch_genius_lyrics import augment_with_genius
from save_spotify_tracks import fetch_saved_tracks


def main():
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <lang1,lang2,...> [min_songs]")
        sys.exit(1)

    languages = sys.argv[1].split(",")
    min_songs = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    print("\n🎵 Stage 1: Fetching Spotify tracks...")
    spotify_file = fetch_saved_tracks()

    print("\n🗣️ Stage 2: Detecting track languages...")
    lang_file = detect_languages(input_file=spotify_file)

    print("\n📝 Stage 3: Fetching Genius lyrics...")
    genius_file = augment_with_genius(input_file=lang_file)

    print("📀 Stage 4: Creating playlists...")
    create_playlists_from_file(
        input_file=genius_file,
        languages=languages,
        min_songs=min_songs
    )

    print("✅ Orchestration complete!")

if __name__ == "__main__":
    main()
