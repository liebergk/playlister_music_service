from flask import Flask
from dotenv import load_dotenv
import os 

load_dotenv()

app = Flask(__name__)

PLAYLIST_ID = ''
load_dotenv()

@app.route("/")
def hello_world():
    spotify_client_id = os.environ.get("spotifyClientId")
    spotify_secret = os.environ.get("spotifySecret")
    return "<p>userID= " + spotify_client_id + "; key = " + spotify_secret + "</p>"

@app.route("/songs", methods=['PUT', 'GET'])
def add_song():
    return "<p>UNDER CONSTRUCTION</p>"
    