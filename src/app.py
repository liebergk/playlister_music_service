from flask import Flask

app = Flask(__name__)

PLAYLIST_ID = ''

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/songs", methods=['PUT', 'GET'])
def add_song():
    return "<p>UNDER CONSTRUCTION</p>"