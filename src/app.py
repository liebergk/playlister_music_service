from flask import Flask, request
import music

app = Flask(__name__)

@app.route("/")
def root():
    return ""

@app.route("/services/<service_name>/playlists/<playlist_name>", methods=['GET'])
def get_playlist_by_name(service_name: str, playlist_name: str):
    service: music.MusicService = music.services.get(service_name.upper())
    response_code = 200
    response_body = None
    try:
        response_body = service.get_playlist(playlist_name=playlist_name)._asdict()
        print(response_body)
    except:
        response_code = 500
        response_body = "Unable to find playlist. Internal server error"
    return response_body, response_code

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

@app.route("/services/<service_name>/playlists/<playlist_name>/tracks", methods=['POST'])
def add_track_to_playlist(service_name: str, playlist_name):

    service: music.MusicService = music.services.get(service_name.upper())

    service.add_track_to_playlist(playlist_name=playlist_name, track_id=request.form['track_id'])
    return ""


    