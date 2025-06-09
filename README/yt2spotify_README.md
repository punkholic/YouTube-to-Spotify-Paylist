# YouTube to Spotify Playlist Migrator

This script allows you to migrate your YouTube playlists to Spotify playlists. It uses the YouTube Data API (via yt-dlp) and Spotify Web API to transfer your music.

## Prerequisites

- Python 3.6 or higher
- A Spotify account
- A YouTube playlist URL
- YouTube Data API v3 enabled in Google Cloud Console

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Spotify credentials:
   - Create a `.env` file in the project directory
   - Add your Spotify credentials:
   ```
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=your_spotify_redirect_uri
   ```

## Usage

1. Basic usage (with default playlist name):
```bash
python yt2spotify.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

2. With custom playlist name:
```bash
python yt2spotify.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID" --playlist_name "My Custom Playlist"
```

3. Delete existing playlist with same name:
```bash
python yt2spotify.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID" --playlist_name "My Custom Playlist" --delete
```

Command-line Arguments:
- `--playlist_url` (required): The URL of your YouTube playlist
- `--playlist_name`: Name for the Spotify playlist (default: "youtube")
- `--delete`: Delete existing playlist with same name without prompting

The script will:
- Extract song titles from the YouTube playlist
- Clean and parse the titles to extract artist and song names
- Search for each song on Spotify
- Create a new private Spotify playlist (or use existing one)
- Add the found songs to the playlist
- Save progress to a pickle file for resuming if needed

## Features

- Migrates entire YouTube playlists to Spotify
- Smart title parsing to extract artist and song names
- Handles rate limiting and retries
- Creates private playlists by default
- Batch processing to avoid API limits
- Progress saving and resuming
- Duplicate track prevention
- Error handling and retries

## Notes

- The script creates a pickle file to store track URIs for resuming
- Spotify playlists are created as private by default
- The script uses the first search result for each song
- Rate limiting is implemented to avoid API quota issues
- Title parsing removes common YouTube video indicators (e.g., "official", "lyrics", "video")

## Troubleshooting

1. If songs aren't being found:
   - The title parsing might not be accurate for some formats
   - Try modifying the `extract_song_name` function for your specific playlist format

2. If you get authentication errors:
   - Make sure your Spotify credentials are correct in the `.env` file
   - Verify that you've granted the necessary permissions

3. If the script stops unexpectedly:
   - Check the pickle file for saved progress
   - Run the script again with the same parameters to resume

## License

This project is licensed under the MIT License - see the LICENSE file for details. 