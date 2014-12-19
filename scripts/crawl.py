import sys
import spotipy
import spotipy.util as util
import pprint as pp
import cPickle as pickle
import atexit
import os

max_playlists = 10000
scope = 'user-library-read'


def is_good_playlist(items):
    artists = set()
    albums = set()
    for item in items:
        track = item['track']
        if track:
            artists.add( track['artists'][0]['id'])
            albums.add(track['album']['id'])
    return len(artists) > 1 and len(albums) > 1

def process_playlist(which, total, playlist):
    tracks = data['tracks']

    print which, total, data['ntracks'], len(tracks), playlist['name']

    pid = playlist['id']
    uid = playlist['owner']['id']
    data['playlists'] += 1

    try:
        results = sp.user_playlist_tracks(uid, playlist['id'])
        # fields="items.track(!album)")

        if results and 'items' in results and is_good_playlist(results['items']):
            for item in results['items']:
                track = item['track']
                if track:
                    tid = track['id']
                    if tid not in tracks:
                        title = track['name'] 
                        artist = track['artists'][0]['name']
                        tracks[tid] = {
                            'title' : title,
                            'artist' : artist,
                            'count' : 0,
                        }
                    tracks[tid]['count'] += 1
                    data['ntracks'] += 1
        else:
            print 'mono playlist skipped'
    except spotipy.SpotifyException:
        print 'trouble, skipping'

def save():
    out = open('tracks.pkl', 'w')
    pickle.dump(data, out, -1)
    out.close()

def load():
    if os.path.exists('tracks.pkl'):
        infile = open('tracks.pkl')
        data = pickle.load(infile)
    else:
        data = {
            'playlists': 0,
            'ntracks': 0,
            'offset': -1,
            'tracks': {}
        }
    return data

    
def crawl_playlists():
    queries = ['the']
    limit = 50

    for query in queries:
        which = 0
        offset = 0 if data['offset'] < 0 else data['offset'] + limit
        results = sp.search(query, limit=limit, offset=offset, type='playlist')
        playlist = results['playlists']
        total = playlist['total']
        while playlist:
            data['offset'] = playlist['offset'] + playlist['limit']
            for item in playlist['items']:
                process_playlist(which, total, item)
                which += 1

            if playlist['next']:
                results = sp.next(playlist)
                playlist = results['playlists']
            else:
                playlist = None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        atexit.register(save)
        data = load()
        crawl_playlists()
    else:
        print "Can't get token for", username
