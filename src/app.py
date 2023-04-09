from flask import Flask
import music

app = Flask(__name__)

@app.route("/")
def root():
    return ""

@app.route("/playlists", methods=['GET'])
def get_playlists():
    # scope = "playlist-read-private"

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    # user_id = sp.current_user()['id']

    # playlists = sp.user_playlists(user_id)
    # while playlists:
    #     for i, playlist in enumerate(playlists['items']):
    #         print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    #     if playlists['next']:
    #         playlists = sp.next(playlists)
    #     else:
    #         playlists = None
    return ""

@app.route("/services/<service_name>/playlists/<playlist_name>", methods=['POST'])
def create_playlist(service_name: str, playlist_name):
    service: music.MusicService = music.services.get(service_name.upper())

    resp = service.create_playlist(playlist_name=playlist_name)
    return ""

@app.route("/services/<service_name>/playlists/<playlist>/tracks", methods=['GET'])
def get_songs(service_name: str, playlist):
    
    # scope = "playlist-read-private"

    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    # user_id = sp.current_user()['id']

    # tracks = sp.user_playlist_tracks(user_id, playlist_id=playlist_id)
    track_list = []
    # while tracks:
    #     for i, track in enumerate(tracks['items']):
    #         track_list.append(track['track']['id'])
    #     if tracks['next']:
    #         tracks = sp.next(tracks)
    #     else:
    #         tracks = None
    return "<p>" + '</p><p>'.join(track_list) + "</p>"

@app.route("/services/<service_name>/playlists/<playlist>/track/<track>", methods=['PUT'])
def add_track_to_playlist(service_name: str, playlist, track):

    service: music.MusicService = music.services.get(service_name.upper())

    service.add_track_to_playlist(playlist=playlist, track=track)
    return ""


    