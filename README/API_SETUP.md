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
   - Redirect URI: `https://localhost:8888/callback`
5. Accept the terms and click "Create"
6. Once created, you'll see your:
   - Client ID
   - Client Secret
7. Add these to your `.env` file:
   ```
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=https://localhost:8888/callback
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
     - `http://localhost:8080/`
   - Click "Save"

## Verifying Your Setup

1. Check your `.env` file has the correct Spotify credentials:
   ```
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=https://localhost:8888/callback
   ```

2. Verify `client_secrets.json` is in your project directory

3. Run the script:
   ```bash
   python spotify2yt.py  # or yt2spotify.py
   ```

## Troubleshooting

### Spotify API Issues
- If you get "Invalid client" error:
  - Double-check your Client ID and Secret
  - Make sure they're correctly copied to `.env`
- If you get "Invalid redirect URI" error:
  - Verify the redirect URI matches exactly in both Spotify Dashboard and `.env`

### YouTube API Issues
- If you get "redirect_uri_mismatch" error:
  - Add `http://localhost:8080/` to authorized redirect URIs
- If you get "access_denied" error:
  - Make sure you're added as a test user
  - Verify the YouTube scope is added
- If you get "quota exceeded" error:
  - YouTube API has daily quotas
  - Consider implementing caching or rate limiting

## Security Notes

- Never commit your `.env` file or `client_secrets.json` to version control
- Keep your API credentials secure
- Regularly rotate your credentials if they're compromised
- Use environment variables in production

## Additional Resources

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) 
