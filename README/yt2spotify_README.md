# Spotify-YouTube Playlist Migrator

A collection of scripts to migrate playlists between Spotify and YouTube. This repository contains two main scripts:

1. [YouTube to Spotify Playlist Migrator](yt2spotify_README.md) - Migrate playlists from YouTube to Spotify
2. [Spotify to YouTube Playlist Migrator](spotify2yt_README.md) - Migrate playlists from Spotify to YouTube

## Overview

This project provides tools to help you transfer your music playlists between Spotify and YouTube. Whether you're moving from one platform to another or just want to have your playlists available on both platforms, these scripts make the process easy and automated.

## Features

- Bidirectional playlist migration
- Maintains song order
- Handles rate limiting
- Batch processing
- Progress tracking
- Error handling
- Private playlist support

## Quick Start

1. Clone this repository:
```bash
git clone https://github.com/yourusername/spotify-youtube-migrator.git
cd spotify-youtube-migrator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Choose your migration direction:
   - For YouTube to Spotify: See [YouTube to Spotify Guide](yt2spotify_README.md)
   - For Spotify to YouTube: See [Spotify to YouTube Guide](spotify2yt_README.md)

## Requirements

- Python 3.6 or higher
- Spotify account
- Google account
- YouTube Data API v3 enabled
- Required Python packages (see requirements.txt)

## Project Structure

```
spotify-youtube-migrator/
├── README.md                 # This file
├── yt2spotify_README.md      # YouTube to Spotify documentation
├── spotify2yt_README.md      # Spotify to YouTube documentation
├── yt2spotify.py            # YouTube to Spotify script
├── spotify2yt.py            # Spotify to YouTube script
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create this)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Spotipy](https://github.com/spotipy-dev/spotipy) - Spotify Web API wrapper
- [Google API Python Client](https://github.com/googleapis/google-api-python-client) - YouTube Data API wrapper 