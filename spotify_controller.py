from spotify_api_requests import play_music
from spotify_tokens_api import get_access_token
from spotify_tokens_api import check_access_token

def spotify_play_music(spotify_uri):
    check_access_token()
    access_token = get_access_token()
    play_music(access_token, spotify_uri)

spotify_play_music("spotify:playlist:37i9dQZF1DX6J5NfMJS675")