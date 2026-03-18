"use strict";

var SPOTIFY_CLIENT_ID = '4042a231fe624583a694f1d6cf9e25b5';
var SPOTIFY_REDIRECT_URI = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
    ? 'http://127.0.0.1:8000/'
    : 'http://playlistminer.playlistmachinery.com/';
