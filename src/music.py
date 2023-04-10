import spotipy
from spotipy.oauth2 import SpotifyOAuth
import object_factory
from music_type_definitions import *

_PLAYLISTER_APP_USER_ID='31wrypfeq4b4b5imyxlm2izeihxa'

class MusicProviderNotFoundException(Exception):
    """Exception for unrecognized Music Providers"""
    pass

class MusicServiceFactory(object_factory.ObjectFactory):
    def get(self, service_id, **kwargs):
        return self.create(service_id, **kwargs)

class MusicService:
    """
    MusicService represents the service providing music to a user. Such a 
    service should be able to find and play tracks, organize playlists, and
    otherwise help the user organizer their music in a consistent way across
    platforms
    """
    def __init__(self) -> None:
        pass
    
    def get_playlist(self, playlist_name: str) -> Playlist:
        raise NotImplementedError("get_playlist not implemented")
    
    def get_playlists(self) -> list[Playlist]:
        raise NotImplementedError("get_playlists not implemented")
    
    def create_playlist(self, playlist_name) -> Playlist:
        raise NotImplementedError("create_playlist not implemented")
    
    def add_track_to_playlist(self, playlist_name, track_id) -> Track:
        raise NotImplementedError("add_song_to_playlist not implemented")
    
    def add_tracks_to_playlist(self, playlist_id, tracks: list[Track]) -> list[Track]:
        for track in tracks:
            self.add_track_to_playlist(playlist_id, track.id)
    
class SpotifyService(MusicService):
    
    def __init__(self) -> None:
        super().__init__()

    def get_playlists(self) -> list[Playlist]:
        scope='playlist-read-collaborative'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        query_response = sp.user_playlists(sp.current_user()['id'])
        playlists = {}
        while query_response:
            for item in query_response['items']:
                playlists[item['name']] = Playlist(id=item['id'], name=item['name'], 
                                                owner_id=item['owner']['id'])
            if query_response['next']:
                query_response = self._sp.next(query_response)
            else:
                query_response = None
        return playlists

    def get_playlist(self, playlist_name: str) -> Playlist:
        playlists = self.get_playlists()
        return playlists.get(playlist_name)


    def create_playlist(self, playlist_name: str) -> Playlist:
        scope='playlist-modify-public'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        resp = sp.user_playlist_create(user=_PLAYLISTER_APP_USER_ID, name=playlist_name, public=True)
        return resp
    
    def add_track_to_playlist(self, playlist_name, track_id) -> Track:
        scope='playlist-modify-public'
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        playlist_id = self.get_playlist(playlist_name=playlist_name).id
        return sp.user_playlist_add_tracks(_PLAYLISTER_APP_USER_ID, playlist_id, tracks=[track_id])


class SpotifyServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = SpotifyService()
        return self._instance
    
class YoutubeService(MusicService):
    def __init__(self) -> None:
        super().__init__()

    def add_track_to_playlist(self, playlist, track):
        pass

class YoutubeServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = YoutubeService()
        return self._instance
    
class TidalService(MusicService):
    def __init__(self) -> None:
        super().__init__()

    def add_track_to_playlist(self, playlist, track):
        pass

class TidalServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = TidalService()
        return self._instance
    
services = MusicServiceFactory()
services.register_builder('SPOTIFY', SpotifyServiceBuilder())
services.register_builder('YOUTUBE', YoutubeServiceBuilder())
services.register_builder('TIDAL', TidalServiceBuilder())