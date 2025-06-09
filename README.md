# Spotify-YouTube Playlist Migrator

A collection of scripts to migrate playlists between Spotify and YouTube. This repository contains two main scripts:


## Navigation

- [API Setup Guide](README/API_SETUP.md) - Detailed instructions for setting up Spotify and YouTube API credentials
- [YouTube to Spotify Guide](README/yt2spotify_README.md) - Complete guide for migrating from YouTube to Spotify
- [Spotify to YouTube Guide](README/spotify2yt_README.md) - Complete guide for migrating from Spotify to YouTube

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
git clone https://github.com/punkholic/spotify-youtube-migrator.git
cd spotify-youtube-migrator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API credentials:
   - See [API Setup Guide](README/API_SETUP.md) for detailed instructions on setting up Spotify and YouTube API credentials

4. Choose your migration direction:
   - For YouTube to Spotify: See [YouTube to Spotify Guide](README/yt2spotify_README.md)
   - For Spotify to YouTube: See [Spotify to YouTube Guide](README/spotify2yt_README.md)

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
├── README/                   # Documentation directory
│   ├── API_SETUP.md         # API credentials setup guide
│   ├── yt2spotify_README.md  # YouTube to Spotify documentation
│   └── spotify2yt_README.md  # Spotify to YouTube documentation
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