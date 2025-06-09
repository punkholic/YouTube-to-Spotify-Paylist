# Spotify to YouTube Playlist Migrator

This script allows you to migrate your Spotify playlists or liked songs to YouTube playlists. It uses the Spotify Web API and YouTube Data API v3 to transfer your music.

## Prerequisites

- Python 3.6 or higher
- A Spotify account
- A Google account
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

3. Set up YouTube API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Go to "Credentials"
   - Create OAuth 2.0 Client ID (Desktop application)
   - Download the credentials and save as `client_secrets.json` in the project directory

4. Configure OAuth consent screen:
   - Go to "OAuth consent screen" in Google Cloud Console
   - Choose "External" user type
   - Fill in the required information
   - Add your email as a test user
   - Add the scope: `https://www.googleapis.com/auth/youtube`

## Usage

1. Migrate a Spotify playlist (basic usage):
```bash
python spotify2yt.py "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID"
```

2. Migrate liked songs:
```bash
python spotify2yt.py --liked-songs
```

3. Migrate liked songs with custom name:
```bash
python spotify2yt.py --liked-songs --name "My Liked Songs"
```

4. Migrate a playlist with custom name:
```bash
python spotify2yt.py "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID" --name "My Custom Playlist"
```

5. With custom name and description:
```bash
python spotify2yt.py "https://open.spotify.com/playlist/YOUR_PLAYLIST_ID" --name "My Custom Playlist" --description "My favorite songs"
```

Command-line Arguments:
- `spotify_url` (optional): The URL of your Spotify playlist (required if not using --liked-songs)
- `--liked-songs`: Flag to migrate liked songs instead of a playlist
- `--name`: Custom name for the YouTube playlist (default: "Spotify Playlist" or "Liked Songs")
- `--description`: Custom description for the YouTube playlist (default: "Migrated from Spotify")

The script will:
- Open your browser for YouTube authentication
- Fetch tracks from your Spotify playlist or liked songs
- Create a new private YouTube playlist
- Search for each song on YouTube
- Add the found videos to your playlist

## Features

- Migrates entire Spotify playlists to YouTube
- Migrates liked songs to YouTube
- Maintains song order
- Handles rate limiting
- Creates private playlists by default
- Batch processing to avoid API limits
- Progress tracking
- Error handling
- Custom playlist naming and description
- Support for Spotify playlist URLs

## Notes

- The script creates a `token.pickle` file to store YouTube credentials
- YouTube playlists are created as private by default
- The script uses the first search result for each song
- Rate limiting is implemented to avoid API quota issues
- When migrating liked songs, the playlist will be named "Liked Songs" by default

## Troubleshooting

1. If you get "redirect_uri_mismatch" error:
   - Add `http://localhost:8080/` to authorized redirect URIs in Google Cloud Console

2. If you get "access_denied" error:
   - Make sure you've added your email as a test user in OAuth consent screen
   - Verify that you've added the YouTube scope

3. If videos aren't being found:
   - The search might not find exact matches
   - Try modifying the search query format in the code

## License

This project is licensed under the MIT License - see the LICENSE file for details. 