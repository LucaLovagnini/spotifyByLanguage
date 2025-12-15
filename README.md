# 🎵 Spotify Playlist by Language

Automatically organize your Spotify saved tracks into language-specific playlists using AI-powered language detection and lyrics analysis.

## ✨ Features

- **Smart Language Detection**: Uses metadata (track names, artists, albums) and lyrics from Genius to detect song languages
- **Multi-Language Support**: Create playlists for multiple languages simultaneously
- **Intelligent Fallback**: Falls back to Genius lyrics when metadata-based detection is uncertain
- **Batch Processing**: Efficiently handles large music libraries
- **Rate Limit Handling**: Built-in retry logic for API rate limits
- **Resume Support**: Can resume interrupted operations

## 🚀 How It Works

1. **Fetch Tracks**: Retrieves all your saved Spotify tracks
2. **Language Detection**: Analyzes track metadata with weighted scoring
3. **Lyrics Enhancement**: Uses Genius API for uncertain cases
4. **Playlist Creation**: Automatically creates organized playlists in your Spotify account

## 📋 Prerequisites

- Python 3.9+
- Spotify Premium account (recommended)
- Spotify Developer App credentials
- Genius API token (optional but recommended)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LucaLovagnini/spotifyByLanguage
   cd spotifyByLanguage
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API credentials:
   ```
    # Spotify API credentials
    SPOTIPY_CLIENT_ID=your_spotify_client_id_here
    SPOTIPY_CLIENT_SECRET=your_spotify_client_secret_here
    SPOTIPY_REDIRECT_URI=http://127.0.0.1:7777/callback
    
    # Genius API (optional)
    GENIUS_ACCESS_TOKEN=your_genius_token_here
   ```

## 🔑 API Setup

### Spotify API
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note down your `Client ID` and `Client Secret`
4. Add `http://127.0.0.1:7777/callback` to Redirect URIs
5. Under Which API/SDKs are you planning to use? select Web Api

### Genius API
1. Go to [Genius API](https://genius.com/api-clients)
2. Create a new API client
3. For App Website URL use https://localhost
4. Generate an access token

## 🎯 Usage

### Quick Start

```bash
python orchestratory.py en,es,fr
```

This creates playlists for English, Spanish, and French songs.

### Advanced Usage

````bash 
python orchestratory.py en,es,fr,de,it 15
````

Creates playlists for 5 languages, requiring at least 15 songs per playlist.

### Individual Modules
You can also run individual stages:

```bash
# Stage 1: Fetch Spotify tracks
python save_spotify_tracks.py

# Stage 2: Detect languages
python detect_language.py

# Stage 3: Enhance with Genius lyrics
python fetch_genius_lyrics.py

# Stage 4: Create playlists
python create_playlist.py data/language_identified_genius.json en,es,fr
```

## 📊 Language Detection Algorithm

### 📋 Supported Languages
The system supports all languages detected by the `langdetect` library, including:
- **en** — English
- **es** — Spanish
- **fr** — French
- **de** — German
- **it** — Italian
- **pt** — Portuguese
- **ru** — Russian
- **ja** — Japanese
- **ko** — Korean
- **zh** — Chinese
- And many more...

### 🚩Known Limitations

- **Instrumental tracks** (i.e., tracks without lyrics) are currently classified as `unknown`. Support for explicit 
instrumental detection is planned via the `tag_instrumentals` step in a future release.

- **Metadata-based language detection may be inaccurate.** The initial classification step runs `langdetect` on a 
combination of track title, artist name, and album name. This can lead to incorrect results when the title language 
differs from the lyric language (e.g., *Madonna – La Isla Bonita* is classified as `es` based on the title, 
even though the lyrics are primarily in English).

## ⚙️ Configuration
### Language Detection Settings
You can modify these in : `config.py`
- Minimum confidence (default: 0.80) `LANGUAGE_CONF_THRESHOLD`
- Field importance weights `WEIGHTS`
- Minimum text length `MIN_TEXT_LEN`

### Rate Limiting
Built-in rate limiting with exponential backoff:
- Spotify: 50 songs fetched per request
- Genius: 1-second between requests, with progressive delays on rate limits

## 🔍 Troubleshooting
### Common Issues
**"No module named 'spotipy'"**
``` bash
pip install -r requirements.txt
```
**"Invalid client credentials"**
- Check your Spotify API credentials in `.env`
- Ensure redirect URI matches exactly

**"Rate limit exceeded"**
- For Genius, the script handles this automatically with retries and exponential backoff
- For Spotify, reduce the number of fetched songs per request through `FLUSH_INTERVAL`

**"Permission denied" for playlists**
- Ensure your Spotify app has the correct scopes
- Re-authenticate by deleting file `.cache`

## ⚠️ Disclaimer
- This tool accesses your Spotify library and creates playlists
- Language detection accuracy varies by song metadata quality
- Genius lyrics fetching is rate-limited and optional
- Respect API terms of service and rate limits

## 🙏 Acknowledgments
- [Spotipy](https://spotipy.readthedocs.io/) — Spotify Web API wrapper
- [langdetect](https://github.com/Mimino666/langdetect) — Language detection library
- [Genius API](https://docs.genius.com/) — Lyrics and song information
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) — Web scraping

Made with ❤️ for music lovers who appreciate linguistic diversity in their playlists!
