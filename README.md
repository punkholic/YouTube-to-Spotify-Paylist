# YouTube to Spotify Playlist Transfer

This script allows you to transfer songs from a YouTube playlist to a Spotify playlist named "youtube."

## Prerequisites

- Python 3.x
- Required Python packages: `yt-dlp`, `spotipy`, `python-dotenv`

## Setup

1. **Environment Variables**: Create a `.env` file in the same directory as the script with the following variables:
   ```
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   SPOTIPY_REDIRECT_URI=your_redirect_uri
   ```

2. **Install Dependencies**: Run the following command to install the required packages:
   ```sh
   pip install yt-dlp spotipy python-dotenv
   ```

## Usage

Run the script using the following command:
```sh
python3 yt2spotify.py
```

### Custom Arguments

- **Playlist URL**: You can specify a custom YouTube playlist URL using the `--playlist_url` argument:
  ```sh
  python3 yt2spotify.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
  ```

- **Playlist Name**: You can specify a custom name for the Spotify playlist using the `--playlist_name` argument:
  ```sh
  python3 yt2spotify.py --playlist_name "Your Playlist Name"
  ```

- **Delete Existing Playlists**: If you want to delete all existing playlists with the same name without being prompted, use the `--delete` flag:
  ```sh
  python3 yt2spotify.py --delete
  ```

## What the Script Does

1. **Fetches Song Titles**: The script extracts song titles from the specified YouTube playlist.
2. **Purges Titles**: It cleans up the titles to extract just the song names.
3. **Searches on Spotify**: It searches for each song on Spotify and adds the first found match to the specified playlist.
4. **Avoids Duplicates**: The script checks if a song is already in the playlist before adding it.

## Additional Notes

- Ensure that your Spotify app has the necessary permissions to modify playlists.
- The script will prompt you to delete an existing playlist with the same name if it exists, unless the `--delete` flag is used.

## .env Variables

The following environment variables are required in a `.env` file:

- `SPOTIPY_CLIENT_ID`: Your Spotify Client ID.
- `SPOTIPY_CLIENT_SECRET`: Your Spotify Client Secret.
- `SPOTIPY_REDIRECT_URI`: Your Spotify Redirect URI.

## Notes

- Ensure your Spotify app has the necessary permissions to modify playlists.
- The script will print the purged song names and the results of the Spotify search. 