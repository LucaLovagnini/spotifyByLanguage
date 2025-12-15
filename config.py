import os

# Data directory
DATA_DIR = "data"

# File paths - pipeline flow
SPOTIFY_TRACKS = os.path.join(DATA_DIR, "spotify_tracks.json")
TRACKS_TAGGED = os.path.join(DATA_DIR, "tracks_tagged.json")
LANGUAGE_IDENTIFIED = os.path.join(DATA_DIR, "language_identified.json")
LANGUAGE_IDENTIFIED_GENIUS = os.path.join(DATA_DIR, "language_identified_genius.json")

# Processing constants
INSTRUMENTAL_THRESHOLD = 0.9
LANGUAGE_CONF_THRESHOLD = 0.80
MIN_TEXT_LEN = 3
FLUSH_INTERVAL = 50

# Weights for language detection
FIELD_WEIGHTS = {
    "name": 0.5,
    "artist": 0.3,
    "album": 0.2
}

# API URLs
GENIUS_SEARCH_URL = "https://api.genius.com/search"

# Spotify scopes
SPOTIFY_READ_SCOPE = "user-library-read"
SPOTIFY_PLAYLIST_SCOPE = "playlist-modify-public playlist-modify-private"
