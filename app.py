from flask import Flask, request
import music
import logging

app = Flask(__name__)


@app.route("/")
def root():
    return "Hey there, listener!"


@app.route("/services/<service_name>/playlists/<playlist_name>", methods=['GET'])
def get_playlist_by_name(service_name: str, playlist_name: str):
    service: music.MusicService = music.services.get(service_name.upper())

    try:
        return service.get_playlist(playlist_name=playlist_name)._asdict()
    except:
        logging.exception(msg="Error finding playlist", exc_info=True)
        return "Unable to find playlist. Internal server error", 500


@app.route("/services/<service_name>/playlists/<playlist_name>", methods=['POST'])
def create_playlist(service_name: str, playlist_name):
    service: music.MusicService = music.services.get(service_name.upper())

    try:
        return service.create_playlist(playlist_name=playlist_name)._asdict()
    except:
        logging.exception(msg="Error creating playlist", exc_info=True)
        return "Unable to create playlist. Internal server error", 500


@app.route("/services/<service_name>/playlists/<playlist_name>/tracks", methods=['GET'])
def get_tracks(service_name: str, playlist_name):
    service: music.MusicService = music.services.get(service_name.upper())
    try:
        playlist = service.get_playlist(playlist_name=playlist_name, get_tracks=True)
        tracks = playlist.tracks
        return {'tracks': [track._asdict() for track in tracks]}
    except:
        logging.exception(
            msg="Error finding playlist or tracks", exc_info=True)
        return "Unable to find playlist or tracks. Internal server error", 500


@app.route("/services/<service_name>/playlists/<playlist_name>/tracks", methods=['POST'])
def add_tracks_to_playlist(service_name: str, playlist_name):
    service: music.MusicService = music.services.get(service_name.upper())

    try:
        request_body = request.json
        result = service.add_tracks_to_playlist(playlist_name=playlist_name,
                                                tracks=request_body['tracks'])
        return result._asdict()
    except:
        logging.exception(
            msg="Error finding playlist or tracks", exc_info=True)
        return "Unable to add tracks to playlist. Internal server error", 500
