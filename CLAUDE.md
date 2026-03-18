# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Playlist Miner is a client-side web app that finds the most popular tracks across Spotify playlists matching a keyword search. Users log in with Spotify, enter search terms (e.g. "workout"), and the app aggregates tracks from up to 1000 matching playlists to surface the top 100 most frequently occurring songs, which can be saved as a new Spotify playlist.

## Architecture

**Single-page app** — all application logic lives inline in `index.html` as vanilla JavaScript (jQuery + Underscore.js). There is no build step, bundler, or framework.

### Key flow:
1. **Auth**: Spotify OAuth Authorization Code + PKCE flow (`authorizeUser()` / `exchangeCodeForToken()`). Refresh token cached in `localStorage` for session persistence across page loads.
2. **Playlist search**: `findMatchingPlaylists()` — searches Spotify API for playlists matching keywords, paging sequentially via Spotify's `next` URL. Includes 429 retry with `Retry-After` backoff.
3. **Track aggregation**: `fetchAllTracksFromPlaylist()` — fetches tracks from each playlist (max 6 simultaneous requests with 429 retry/backoff), counts occurrences, filters out "mono" playlists (single artist/album).
4. **Scoring**: `getTrackScore()` — either raw count or popularity-normalized score (toggled by "Prefer more distinctive tracks" checkbox).
5. **Save**: `savePlaylist()` — creates a new Spotify playlist and adds the top 100 tracks.

### Files:
- `index.html` — the entire app (HTML + inline JS)
- `config.js` — Spotify client ID and redirect URI (auto-detects localhost vs production)
- `styles.css` — custom styles
- `dist/` — Spotify-themed Bootstrap CSS and fonts (only `sp-bootstrap.min.css` and glyphicons are used)
- `lib/` — vendored jQuery 1.11.1, Bootstrap, Underscore.js

### Scripts (`scripts/`):
Python 2 scripts for generating track popularity data used for the "distinctiveness" scoring feature:
- `crawl.py` — crawls Spotify playlists via spotipy, saves track counts to `tracks.pkl`. Usage: `python crawl.py <spotify_username>`
- `proc.py` — reads `tracks.pkl`, outputs `ppm.js` (track frequency JSON). Copy to root dir to use.

## Development

Serve locally with any static file server on port 8000:
```
python -m http.server 8000
```

The whitelisted local redirect URI is `http://127.0.0.1:8000/` — access the app via that address, not `localhost`.

## Deployment

```
./deploy
```

Rsyncs to `/home/www/playlistminer/` on the production Linode (50.116.51.150), excluding `.git`, `CLAUDE.md`, `README.md`, and `scripts/`.

The server runs nginx with SSL via Let's Encrypt/Certbot. Config is at `/etc/nginx/sites-available/playlistminer`.

## Key Details

- Spotify client ID and redirect URIs are in `config.js`
- Production URL: `https://playlistminer.playlistmachinery.com/`
- No tests, no linter, no build process
- The `scripts/` directory uses Python 2 (cPickle, print statements)
- Sister app OrganizeYourMusic (`../OrganizeYourMusic`) uses the same auth pattern

## Spotify API Notes

- Search API caps results for generic/popular terms (e.g. "chill" returns ~150 results while "chill beats" returns ~800) — this is a Spotify-side limitation
- Rate limiting (429s) is common with concurrent requests — both search and track fetch loops include retry with `Retry-After` backoff
- Always page search results sequentially using the `next` URL from each response, not by calculating offsets upfront
