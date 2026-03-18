# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Playlist Miner is a client-side web app that finds the most popular tracks across Spotify playlists matching a keyword search. Users log in with Spotify, enter search terms (e.g. "workout"), and the app aggregates tracks from up to 1000 matching playlists to surface the top 100 most frequently occurring songs, which can be saved as a new Spotify playlist.

## Architecture

**Single-page app** — all application logic lives inline in `index.html` as vanilla JavaScript (jQuery + Underscore.js). There is no build step, bundler, or framework.

### Key flow:
1. **Auth**: Spotify OAuth implicit grant flow (`loginWithSpotify()` / `performAuthDance()`). Credentials cached in `localStorage`.
2. **Playlist search**: `findMatchingPlaylists()` — searches Spotify API for playlists matching keywords, paginating up to `maxPlaylists` (1000) results with up to 50 concurrent requests.
3. **Track aggregation**: `fetchAllTracksFromPlaylist()` — fetches tracks from each playlist (max 10 simultaneous requests), counts occurrences, filters out "mono" playlists (single artist/album). Tracks scored by raw count or distinctiveness.
4. **Scoring**: `getTrackScore()` — either raw count or popularity-normalized score (toggled by "Prefer more distinctive tracks" checkbox).
5. **Save**: `savePlaylist()` — creates a new Spotify playlist and adds the top 100 tracks.

### Files:
- `index.html` — the entire app (HTML + inline JS)
- `styles.css` — custom styles
- `dist/` — Spotify-themed Bootstrap CSS and fonts
- `lib/` — vendored jQuery 1.11.1, Bootstrap, Underscore.js
- `redirect.html` — legacy redirect from old "CrowdLister" name

### Scripts (`scripts/`):
Python 2 scripts for generating track popularity data used for the "distinctiveness" scoring feature:
- `crawl.py` — crawls Spotify playlists via spotipy, saves track counts to `tracks.pkl`. Usage: `python crawl.py <spotify_username>`
- `proc.py` — reads `tracks.pkl`, outputs `ppm.js` (track frequency JSON). Copy to root dir to use.

## Development

Serve locally with any static file server:
```
python -m http.server 8000
# or
python -m SimpleHTTPServer 8000
```

The app auto-detects localhost and adjusts the OAuth redirect URI accordingly.

## Deployment

Two deploy scripts exist:
- `deploy` — syncs to S3 (`s3://static.echonest.com/playlistminer/`)
- `deploy2` — rsyncs to `playlistmachinery.com`

## Key Details

- Spotify client ID is hardcoded in `index.html` (`loginWithSpotify()`)
- OAuth redirect URI for production: `http://playlistminer.playlistmachinery.com/`
- No tests, no linter, no build process
- The `scripts/` directory uses Python 2 (cPickle, print statements)
