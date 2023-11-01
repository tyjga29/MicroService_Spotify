from spotify_tokens_api import get_viable_access_token
from spotify_api_requests import *

access_token = None

class Spotify_Metadata:
    is_playing = None
    device_info = {
        "id": None,
        "name": None
    }

    @classmethod
    def set_is_playing(cls):
        data = get_spotify_player_info(access_token)
        cls.is_playing = data.get("is_playing")

    @classmethod
    def set_device_info(cls):
        data = get_spotify_player_info(access_token)
        device_info = data.get("device")
        cls.device_info["id"] = device_info.get("id")
        cls.device_info["name"] = device_info.get("name")

    def update_spotify_metadata():
        Spotify_Metadata.set_is_playing()
        Spotify_Metadata.set_device_info()

access_token = get_viable_access_token()
print(access_token)
metadata = Spotify_Metadata
metadata.update_spotify_metadata()
print(metadata.is_playing)
print(metadata.device_info)
    
