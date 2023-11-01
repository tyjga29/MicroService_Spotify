from spotify_tokens_api import get_access_token, check_access_token
from spotify_api_requests import *

class Spotify_Metadata:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls._instance = super(Spotify_Metadata, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.access_token = None
        self.is_playing = None
        self.device_info = {
            "id": None,
            "name": None
        }

    def set_access_token(self):
        self.access_token = get_access_token()
    
    def set_is_playing(self):
        data = get_spotify_player_info(self.access_token)
        self.is_playing = data.get("is_playing")

    def set_device_info(self):
        data = get_spotify_player_info(self.access_token) 
        if data == False:
            return
        device_info = data.get("device")
        self.device_info["id"] = device_info.get("id")
        self.device_info["name"] = device_info.get("name")

    def update_spotify_metadata(self):
        Spotify_Metadata.set_is_playing(self)
        Spotify_Metadata.set_device_info(self)

    def print_instance(self):
        print("Is Playing:", self.is_playing)
        print("Device Info:", self.device_info)
 
#spotify_metadata = Spotify_Metadata()
#check_access_token()
#spotify_metadata.set_access_token()
#spotify_metadata.update_spotify_metadata()