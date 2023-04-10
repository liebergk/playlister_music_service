import spotipy
from spotipy.oauth2 import SpotifyOAuth
import object_factory
from music_type_definitions import *
import os

_PLAYLISTER_APP_USER_ID = os.environ['PLAYLISTER_APP_USER_ID']


class MusicProviderNotFoundException(Exception):
    """Exception for unrecognized Music Providers"""
    pass


class MusicServiceFactory(object_factory.ObjectFactory):
    def get(self, service_id, **kwargs):
        return self.create(service_id, **kwargs)


class MusicService:
    """
    MusicService represents the service providing music to a user. Such a 
    service should be able to find artists and tracks, manage playlists, and
    otherwise help the user organizer their music in a consistent way across
    platforms.
    """

    def __init__(self) -> None:
        pass

    def get_playlist(self, playlist_name: str, get_tracks: bool) -> Playlist:
        raise NotImplementedError("get_playlist not implemented")

    def get_playlists(self) -> list[Playlist]:
        raise NotImplementedError("get_playlists not implemented")

    def create_playlist(self, playlist_name) -> Playlist:
        raise NotImplementedError("create_playlist not implemented")

    def add_tracks_to_playlist(self, playlist_id, tracks) -> list[Track]:
        raise NotImplementedError("add_tracks_to_playlist not implemented")


class SpotifyService(MusicService):

    def __init__(self, spotify_client) -> None:
        super().__init__()
        self._sp = spotify_client or spotipy.Spotify()

    def get_playlist(self, playlist_name: str, get_tracks=False) -> Playlist:
        playlists = self.get_playlists()
        playlist: Playlist = playlists.get(playlist_name)

        if get_tracks:
            playlist = playlist._replace(tracks=self._get_tracks_for_playlist(playlist))

        return playlist
    
    def get_playlists(self) -> list[Playlist]:
        scope = 'playlist-read-collaborative'
        self._sp.auth_manager = SpotifyOAuth(scope=scope)

        query_response = self._sp.user_playlists(self._sp.current_user()['id'])
        playlists = {}

        while query_response:
            for item in query_response['items']:
                playlists[item['name']] = Playlist(
                    id=item['id'],
                    name=item['name'],
                    owner_id=item['owner']['id']
                )
            if query_response['next']:
                query_response = self._sp.next(query_response)
            else:
                query_response = None
        return playlists

    def _get_tracks_for_playlist(self, playlist: Playlist) -> list[Track]:
        scope = 'playlist-read-collaborative'
        self._sp.auth_manager = SpotifyOAuth(scope=scope)

        track_fields = 'items(track(id, name, album(name, id), artists(name, id)))'
        track_response = self._sp.playlist_tracks(
            playlist_id=playlist.id, fields=track_fields)
        tracks = []
        while track_response:
            for _, item in enumerate(track_response['items']):
                tracks.append(
                    Track(
                        id=item['track']['id'],
                        name=item['track']['name'],
                        album=Album(
                            id=item['track']['album']['id'],
                            name=item['track']['album']['name']
                        ),
                        # TODO: Support multi-artist tracks
                        artist=Artist(
                            id=item['track']['artists'][0]['id'],
                            name=item['track']['artists'][0]['name']
                        )
                    )
                )

            # TODO: spotipy.playlist_tracks - response does not include a 'next'.
            # Need to determine whether this is a bug and how to handle it for
            # playlists longer than the default limit

            # if track_response['next']:
            #     track_response = self._sp.next(track_response)
            # else:
            track_response = None

        return tracks

    def create_playlist(self, playlist_name: str) -> Playlist:
        scope = 'playlist-modify-public'
        self._sp.auth_manager = SpotifyOAuth(scope=scope)
        self._sp.user_playlist_create(
            user=_PLAYLISTER_APP_USER_ID, name=playlist_name, public=True)
        
        return self.get_playlist(playlist_name=playlist_name)

    def add_tracks_to_playlist(self, playlist_name, tracks) -> Playlist:
        scope = 'playlist-modify-public'
        self._sp.auth_manager = SpotifyOAuth(scope=scope)

        playlist_id = self.get_playlist(playlist_name=playlist_name).id
        self._sp.user_playlist_add_tracks(user=_PLAYLISTER_APP_USER_ID, playlist_id=playlist_id, tracks=tracks)

        return self.get_playlist(playlist_name=playlist_name, get_tracks=True)


class SpotifyServiceBuilder:
    def __init__(self):
        self._instance = None

    def __call__(self, spotify_client=None, use_cached_instance=True, **_ignored):
        if not self._instance or not use_cached_instance:
            self._instance = SpotifyService(spotify_client)
        return self._instance


class YoutubeService(MusicService):
    def __init__(self) -> None:
        super().__init__()

    def add_tracks_to_playlist(self, playlist_id, tracks):
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

    def add_tracks_to_playlist(self, playlist_id, tracks):
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
