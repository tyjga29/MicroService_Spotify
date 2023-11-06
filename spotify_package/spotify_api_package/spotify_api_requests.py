import requests
from spotify_package.spotify_api_package.spotify_tokens_api import refresh_spotify_token_manually, get_access_token

def error_response(response):
    print(f"Error: {response.status_code}")
    print(response.text)
    return None

def get_spotify_player_info(access_token):
    url = "https://api.spotify.com/v1/me/player"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # The request was successful, and you can access the response content
        data = response.json()
        return data
    elif response.status_code == 204:
        # Request was succesful nothing is playing
        return False
    else:
        error_response(response)

def play_music(access_token, playlist_uri, position=5, position_ms=0):
    url = "https://api.spotify.com/v1/me/player/play"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "context_uri": playlist_uri,
        "offset": {
            "position": position
        },
        "position_ms": position_ms
    }

    response = requests.put(url, headers=headers, json=data)
    
    # Success
    if response.status_code == 204:
        return
    
    # Invalid Token
    elif response.status_code == 401:
        refresh_spotify_token_manually()
        play_music(get_access_token, playlist_uri)

    # No Active Device
    elif response.status_code == 404:
        return
            
    else:
        error_response(response)
        
    
