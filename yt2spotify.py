import yt_dlp
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import argparse
import pickle
import time

load_dotenv()

def get_playlist_titles(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'ignoreerrors': True,
    }
    titles = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            if not playlist_info:
                print("Could not extract playlist information")
                return []
            for entry in playlist_info['entries']:
                if entry:
                    titles.append(entry.get('title', 'Unknown'))
            return titles
        except Exception as e:
            print(f"Error: {str(e)}")
            return []

def extract_song_name(title):
    
    title = re.sub(r"\[.*?\]|\(.*?\)", "", title)
    title = re.split(r"[-:–—|]", title, maxsplit=1)
    if len(title) > 1:
        title = title[1]
    else:
        title = title[0]
    
    title = re.sub(r"\b(official|video|lyrics?|audio|remastered|live|hd|hq|full album|feat\.?|ft\.?)\b", "", title, flags=re.I)
    title = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$", "", title)
    
    title = re.sub(r"\s+", " ", title)
    return title.strip()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-modify-public playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))
user_id = sp.current_user()['id']

def get_or_create_playlist(playlist_name, delete_existing=False):
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            if delete_existing:
                sp.user_playlist_unfollow(user=user_id, playlist_id=playlist['id'])
                print(f"Deleted playlist: {playlist_name}")
            else:
                response = input(f"Playlist '{playlist_name}' already exists. Do you want to delete it? (y/n): ")
                if response.lower() == 'y':
                    sp.user_playlist_unfollow(user=user_id, playlist_id=playlist['id'])
                    print(f"Deleted playlist: {playlist_name}")
                else:
                    print("Using existing playlist.")
                    return playlist['id']
    new_playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
    print(f"Created playlist: {playlist_name}")
    return new_playlist['id']


def search_track_uris(song_names, playlist_id):
    uris = []
    existing_tracks = set()
    
    results = sp.playlist_tracks(playlist_id)
    for item in results.get('items', []):
        if item.get('track'):
            existing_tracks.add(item['track']['uri'])
    for name in song_names:
        if not name.strip():
            continue
        max_retries = 3
        for attempt in range(max_retries):
            try:
                results = sp.search(q=name, type='track', limit=1)
                tracks = results.get('tracks', {}).get('items', [])
                if tracks:
                    track_uri = tracks[0]['uri']
                    if track_uri not in existing_tracks:
                        uris.append(track_uri)
                        print(f"Found: {name} → {tracks[0]['name']} by {tracks[0]['artists'][0]['name']}")
                    else:
                        print(f"Already in playlist: {name}")
                else:
                    print(f"Not found: {name}")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Retrying search for {name} due to error: {str(e)}")
                    time.sleep(2)  # Wait before retrying
                else:
                    print(f"Failed to search for {name} after {max_retries} attempts: {str(e)}")
    return uris

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transfer songs from a YouTube playlist to a Spotify playlist.')
    parser.add_argument('--playlist_url', type=str, default='https://www.youtube.com/playlist?list=PLo2RLtsf-Zl3r5KoTWIzfFudBx_v0BZb6',
                        help='URL of the YouTube playlist to process')
    parser.add_argument('--playlist_name', type=str, default='youtube',
                        help='Name of the Spotify playlist to create or use')
    parser.add_argument('--delete', action='store_true',
                        help='Delete all existing playlists with the same name without prompting')
    args = parser.parse_args()

    # Extract playlist ID from the URL
    playlist_id_tosave = args.playlist_url.split('list=')[-1]
    pickle_file = f'track_uris_{playlist_id_tosave}.pkl'
    playlist_id = get_or_create_playlist(args.playlist_name, args.delete)

    if os.path.exists(pickle_file):
        print(f"Loading existing track URIs from {pickle_file}.")
        with open(pickle_file, 'rb') as f:
            track_uris = pickle.load(f)
    else:
        print("No existing track URIs found. Searching for new tracks...")
        titles = get_playlist_titles(args.playlist_url)
        purged_titles = [extract_song_name(t) for t in titles]
        print(f"Purged song names: {purged_titles[:10]} ... (total: {len(purged_titles)})")
        track_uris = search_track_uris(purged_titles, playlist_id)
        with open(pickle_file, 'wb') as f:
            pickle.dump(track_uris, f)

    print(f"Found {len(track_uris)} tracks")
    if track_uris:
        # Add tracks in batches of 100
        batch_size = 100
        for i in range(0, len(track_uris), batch_size):
            batch = track_uris[i:i + batch_size]
            try:
                sp.playlist_add_items(playlist_id=playlist_id, items=batch)
                print(f"Added tracks {i + 1} to {i + len(batch)} to playlist.")
            except Exception as e:
                print(f"Error adding tracks {i + 1} to {i + len(batch)}: {str(e)}")
                print("Track URIs saved to 'track_uris.pkl'. You can continue from here on the next run.")
    else:
        print("No valid tracks found to add.") 