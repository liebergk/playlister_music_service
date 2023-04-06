from flask import Flask


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

app = Flask(__name__)

@app.route("/")
def hello_world():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return "<p></p>"

@app.route("/playlists", methods=['GET'])
def get_playlists():
    scope = "playlist-read-private"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    print("Attempting OAuth login")
    playlists = sp.user_playlists('spotify')
    print("Logged in")
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return ""

@app.route("/playlists", methods=['POST'])
def create_playlist():
    return "<p>UNDER CONSTRUCTION</p>"

@app.route("/playlists/<playlist_id>/songs", methods=['GET'])
def get_songs(playlist_id):
    return "<p>UNDER CONSTRUCTION</p>"

@app.route("/playlists/<playlist_id>/songs", methods=['PUT'])
def add_song_to_playlist(playlist_id):
    return "<p>UNDER CONSTRUCTION</p>"


    