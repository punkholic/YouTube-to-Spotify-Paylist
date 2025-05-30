# YouTube to Spotify Playlist Transfer

This script fetches song titles from a YouTube playlist, purges them to extract just the song names, and then adds the first found match for each song to a Spotify playlist named "youtube".

## .env Variables

The following environment variables are required in a `.env` file:

- `SPOTIPY_CLIENT_ID`: Your Spotify Client ID.
- `SPOTIPY_CLIENT_SECRET`: Your Spotify Client Secret.
- `SPOTIPY_REDIRECT_URI`: Your Spotify Redirect URI.

## How to Use

1. **Set Up Environment Variables**:
   - Create a `.env` file in the project directory with the required variables.

2. **Install Dependencies**:
   - Ensure you have the required Python packages installed:
     ```sh
     pip install yt-dlp spotipy python-dotenv
     ```

3. **Run the Script**:
   - Execute the script with the following command:
     ```sh
     python3 yt2spotify.py
     ```

## Running with Arguments

To run the script with a custom YouTube playlist URL, you can modify the `playlist_url` variable in the script or pass it as an argument. For example:

```sh
python3 yt2spotify.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

## What the Script Does

- **Fetches Titles**: Retrieves song titles from the specified YouTube playlist.
- **Purges Titles**: Extracts just the song names by removing artist names, descriptors, and other non-essential text.
- **Searches Spotify**: For each purged song name, it searches Spotify and adds the first found match to the "youtube" playlist.
- **Avoids Duplicates**: Checks if the track already exists in the playlist before adding it.

## Notes

- Ensure your Spotify app has the necessary permissions to modify playlists.
- The script will print the purged song names and the results of the Spotify search. 