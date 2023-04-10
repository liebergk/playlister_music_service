import object_factory as object_factory
import music
from music_type_definitions import *
import spotipy
from unittest.mock import MagicMock

_MOCK_USER_ID = 'user1'
_SPOTIFY_SERVICE_NAME = 'SPOTIFY'

_TEST_TRACK = Track(
    id='track_id',
    name='track name'
)

_TEST_PLAYLIST = Playlist(
    id='playlist_id',
    name='playlist name'
)

_TEST_PLAYLIST_WITH_TRACKS = _TEST_PLAYLIST._replace(tracks=[_TEST_TRACK])

class MockSpotify(spotipy.Spotify):
    def current_user(self):
        return {'id': _MOCK_USER_ID}
    
    def user_playlists(self, user):
        return [_TEST_PLAYLIST]
    
    def user_playlist_create(self, user, name, public):
        pass
    
    def playlist_tracks(self, playlist_id, fields):
        return []
    
    def user_playlist_add_tracks(self, user, playlist_id, tracks, position=None):
        pass

def test_create_playlist_returns_playlist():
    service: music.MusicService = music.services.get(_SPOTIFY_SERVICE_NAME, 
                                                     spotify_client=MockSpotify(), use_cached_instance=False)

    service.get_playlist = MagicMock(return_value=_TEST_PLAYLIST)
    test_result_playlist = service.create_playlist(_TEST_PLAYLIST.name)

    service.get_playlist.assert_called_once_with(playlist_name=_TEST_PLAYLIST.name)
    assert test_result_playlist == _TEST_PLAYLIST

def test_get_playlist_finds_playlist_by_name():
    service: music.MusicService = music.services.get(_SPOTIFY_SERVICE_NAME, 
                                                     spotify_client=MockSpotify(), use_cached_instance=False)

    service.get_playlists = MagicMock(return_value={_TEST_PLAYLIST.name : _TEST_PLAYLIST})

    test_result_playlist = service.get_playlist(_TEST_PLAYLIST.name)

    service.get_playlists.assert_called_once()
    assert test_result_playlist == _TEST_PLAYLIST