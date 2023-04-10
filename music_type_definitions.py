from typing import NamedTuple

# TODO: Revisit whether NamedTuple is necessary/helpful. Encoding/decoding to/from json
#       might be doable in a simpler way
class Artist(NamedTuple):
    id: str
    name: str

class Album(NamedTuple):
    id: str
    name: str

class Track(NamedTuple):
    id: str
    name: str
    artist: Artist = None
    album: Album = None

class Playlist(NamedTuple):
    id: str
    name: str
    owner_id: str = None
    tracks: list[Track] = None