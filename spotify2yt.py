import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import argparse
from dotenv import load_dotenv
import time
import re

load_dotenv()

# Spotify setup
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-read-private playlist-read-collaborative'

# YouTube API setup
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/youtube']

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

def get_youtube_service():
    """Set up YouTube API service."""
    credentials = None
    
    # Load credentials from token.pickle if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If credentials don't exist or are invalid, get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', 
                SCOPES,
                redirect_uri='http://localhost:8080/'
            )
            credentials = flow.run_local_server(port=8080)
        
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

def get_spotify_playlist_tracks(playlist_id):
    """Get all tracks from a Spotify playlist."""
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks

def search_youtube_video(youtube, query):
    """Search for a video on YouTube."""
    try:
        request = youtube.search().list(
            part="snippet",
            q=query,
            type="video",
            maxResults=1
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['id']['videoId']
        return None
    except Exception as e:
        print(f"Error searching YouTube: {str(e)}")
        return None

def create_youtube_playlist(youtube, title, description=""):
    """Create a new YouTube playlist."""
    try:
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        return response['id']
    except Exception as e:
        print(f"Error creating YouTube playlist: {str(e)}")
        return None

def add_to_youtube_playlist(youtube, playlist_id, video_ids):
    """Add videos to a YouTube playlist."""
    try:
        for video_id in video_ids:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            request.execute()
        return True
    except Exception as e:
        print(f"Error adding videos to playlist: {str(e)}")
        return False

def extract_playlist_id(playlist_url):
    """Extract playlist ID from Spotify URL."""
    # Match pattern: /playlist/{id} or playlist/{id}
    pattern = r'playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, playlist_url)
    if match:
        return match.group(1)
    return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Migrate Spotify playlist to YouTube')
    parser.add_argument('spotify_url', help='Spotify playlist URL')
    parser.add_argument('--name', help='YouTube playlist name (default: Spotify Playlist)', default='Spotify Playlist')
    parser.add_argument('--description', help='YouTube playlist description', default='Migrated from Spotify')
    args = parser.parse_args()

    # Extract playlist ID from URL
    playlist_id = extract_playlist_id(args.spotify_url)
    if not playlist_id:
        print("Invalid Spotify playlist URL. Please provide a valid URL.")
        return

    # Set up YouTube API
    print("Setting up YouTube API...")
    youtube = get_youtube_service()
    if not youtube:
        print("Failed to set up YouTube API. Exiting.")
        return

    # Get Spotify playlist tracks
    print(f"Fetching tracks from Spotify playlist...")
    tracks = get_spotify_playlist_tracks(playlist_id)
    
    if not tracks:
        print("No tracks found in the Spotify playlist.")
        return

    # Create YouTube playlist
    print(f"Creating YouTube playlist: {args.name}")
    youtube_playlist_id = create_youtube_playlist(youtube, args.name, args.description)
    
    if not youtube_playlist_id:
        print("Failed to create YouTube playlist.")
        return

    # Search and add tracks
    video_ids = []
    for i, item in enumerate(tracks, 1):
        track = item['track']
        if not track:
            continue
            
        # Create search query from track info
        artist = track['artists'][0]['name']
        title = track['name']
        query = f"{artist} - {title}"
        
        print(f"[{i}/{len(tracks)}] Searching for: {query}")
        video_id = search_youtube_video(youtube, query)
        
        if video_id:
            video_ids.append(video_id)
            print(f"Found: {query}")
        else:
            print(f"Not found: {query}")
        
        # Add tracks in batches of 50 to avoid rate limiting
        if len(video_ids) >= 50:
            print(f"Adding batch of {len(video_ids)} tracks to playlist...")
            add_to_youtube_playlist(youtube, youtube_playlist_id, video_ids)
            video_ids = []
            time.sleep(2)  # Rate limiting precaution

    # Add any remaining tracks
    if video_ids:
        print(f"Adding final batch of {len(video_ids)} tracks to playlist...")
        add_to_youtube_playlist(youtube, youtube_playlist_id, video_ids)

    print("Migration completed!")

if __name__ == "__main__":
    main() 