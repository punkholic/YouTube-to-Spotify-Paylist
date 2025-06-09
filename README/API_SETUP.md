# API Setup Guide

This guide will walk you through setting up the necessary API credentials for both Spotify and YouTube Data API v3.

## Spotify API Setup

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - App name: "Spotify-YouTube Migrator" (or any name you prefer)
   - App description: "A tool to migrate playlists between Spotify and YouTube"
   - Website: (Optional) Your website or GitHub repo
   - Redirect URI: `https://7cfe-2400-1a00-1b2c-5edf-4042-f862-4f9a-3909.ngrok-free.app/callback`
5. Accept the terms and click "Create"
6. Once created, you'll see your:
   - Client ID
   - Client Secret
7. Add these to your `.env` file:
   ```
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=https://7cfe-2400-1a00-1b2c-5edf-4042-f862-4f9a-3909.ngrok-free.app/callback
   ```

## YouTube Data API v3 Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

4. Configure OAuth consent screen:
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in the required information:
     - App name: "Spotify-YouTube Migrator"
     - User support email: Your email
     - Developer contact information: Your email
   - Click "Save and Continue"
   - Add the scope: `https://www.googleapis.com/auth/youtube`
   - Click "Save and Continue"
   - Add test users:
     - Click "ADD USERS"
     - Enter your email address (the one you'll use to run the script)
     - Click "ADD"
     - You can add up to 100 test users
     - Make sure to add all email addresses that will use the application
   - Click "Save and Continue"
   - Review your settings and click "Back to Dashboard"

   > **Important**: If you don't add your email as a test user, you'll get an "access_denied" error when trying to use the application. Only test users can access the application while it's in testing mode.

5. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Name: "Spotify-YouTube Migrator"
   - Click "Create"
   - Download the credentials (JSON file)
   - Rename the downloaded file to `client_secrets.json`
   - Place it in your project directory

6. Configure authorized redirect URIs:
   - Go back to your OAuth 2.0 Client ID
   - Click the edit (pencil) icon
   - Under "Authorized redirect URIs", add:
     - `https://7cfe-2400-1a00-1b2c-5edf-4042-f862-4f9a-3909.ngrok-free.app/`
   - Click "Save"

## Verifying Your Setup

1. Check your `.env` file has the correct Spotify credentials:
   ```
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=https://7cfe-2400-1a00-1b2c-5edf-4042-f862-4f9a-3909.ngrok-free.app/callback
   ```

2. Verify `client_secrets.json`