import spotipy
from spotipy.oauth2 import SpotifyOAuth
import object_factory

class MusicProviderNotFoundException(Exception):
    """Exception for unrecognized Music Providers"""
    pass

class MusicServiceProvider(object_factory.ObjectFactory):
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
    
    def create_playlist(self, playlist_name):
        raise NotImplementedError("create_playlist not implemented")
    
    def add_track_to_playlist(self, playlist, track):
        raise NotImplementedError("add_song_to_playlist not implemented")
    
    def add_tracks_to_playlist(self, playlist, tracks):
        for track in tracks:
            self.add_track_to_playlist(playlist, track)
    
class SpotifyService(MusicService):
    
    def __init__(self) -> None:
        super().__init__()

    def create_playlist(self, playlist_name: str):
        print("creating playlist")
        scope = "playlist-modify-private"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        user_id = sp.current_user()['id']

        resp = sp.user_playlist_create(user=user_id, name=playlist_name, public=False,
                                collaborative=False)
        print(str(resp))
        return resp
    
    def add_track_to_playlist(self, playlist, track):
        scope = "playlist-modify-private"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        user_id = sp.current_user()['id']

        sp.playlist_add_items(user_id, playlist=playlist, items=[track])
        tracks = sp.user_playlist_tracks(user_id, playlist=playlist)
        track_list = []
        while tracks:
            for i, track in enumerate(tracks['items']):
                track_list.append(track['track']['name'])
            if tracks['next']:
                tracks = sp.next(tracks)
            else:
                tracks = None
        print(''.join(track_list))
    

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
    
services = MusicServiceProvider()
services.register_builder('SPOTIFY', SpotifyServiceBuilder())
services.register_builder('YOUTUBE', YoutubeServiceBuilder())
services.register_builder('TIDAL', TidalServiceBuilder())