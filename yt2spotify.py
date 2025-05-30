import yt_dlp
import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import argparse

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

def get_or_create_playlist(playlist_name):
    playlists = sp.current_user_playlists(limit=50)
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
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
    return uris

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Transfer songs from a YouTube playlist to a Spotify playlist.')
    parser.add_argument('--playlist_url', type=str, default='https://www.youtube.com/playlist?list=PLo2RLtsf-Zl3r5KoTWIzfFudBx_v0BZb6',
                        help='URL of the YouTube playlist to process')
    parser.add_argument('--playlist_name', type=str, default='youtube',
                        help='Name of the Spotify playlist to create or use')
    args = parser.parse_args()

    titles = get_playlist_titles(args.playlist_url)
    purged_titles = [extract_song_name(t) for t in titles]
    print(f"Purged song names: {purged_titles[:10]} ... (total: {len(purged_titles)})")

    playlist_id = get_or_create_playlist(args.playlist_name)
    track_uris = search_track_uris(purged_titles, playlist_id)

    if track_uris:
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        print("Added tracks to playlist.")
    else:
        print("No valid tracks found to add.") 