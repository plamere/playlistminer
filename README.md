# The Playlist Miner

The Playlist Miner is a web app that creates Spotify playlists based upon matching
keywords.  

Give The Playlist Miner a keyword or two like "workout" or "happy" and The
Playlist Miner will
find as many Spotify playlists that match those keywords. It will then aggregate
all of the songs across all of these playlists and find the top 100 songs that occur the
most frequently in the matching playlist. These top songs can then be saved
to your own playlist.

The Playlist Miner is online at https://playlistminer.playlistmachinery.com/

It makes use of the Spotify Web API.

## Deployment

Files are deployed via rsync to a Linode server:

```
./deploy
```

This rsyncs the local directory to `/home/www/playlistminer/` on the production server (50.116.51.150).

## Server Setup

The production server runs nginx on Ubuntu with SSL via Let's Encrypt.

The nginx config is at `/etc/nginx/sites-available/playlistminer` (symlinked to `sites-enabled`):

```
server {
    server_name playlistminer.playlistmachinery.com;

    location / {
        alias /home/www/playlistminer/;
        index index.html;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/playlistminer.playlistmachinery.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/playlistminer.playlistmachinery.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}
server {
    listen 80;
    server_name playlistminer.playlistmachinery.com;
    if ($host = playlistminer.playlistmachinery.com) {
        return 301 https://$host$request_uri;
    }
    return 404;
}
```

SSL certificates are managed by Certbot. To set up or renew:
```
certbot --nginx -d playlistminer.playlistmachinery.com
```
