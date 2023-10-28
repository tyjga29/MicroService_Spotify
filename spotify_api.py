import requests
import base64
import time
import webbrowser
import secrets

from constants import Constant

#TODO set when read to true
verify_requests = False

constant = Constant()

client_id = constant.spotify["CLIENT_ID"]
client_secret = constant.spotify["CLIENT_SECRET"]
redirect_uri = constant.spotify["REDIRECT_URI"]

# Cache for storing the access token and its creation time
access_token_cache = {
    "token": None,
    "created_at": 0
}

def get_spotify_access_token(client_id, client_secret):
    current_time = int(time.time())
    
    # Check if the token is cached and not older than 50 minutes
    if access_token_cache["token"] and current_time - access_token_cache["created_at"] < 3000:
        return access_token_cache["token"]
    
    # Encode the client ID and client secret to create the Basic Auth header
    auth_header = 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    # Define the payload
    payload = {
        'grant_type': 'client_credentials'
    }

    # Define the headers with the Authorization header
    headers = {
        'Authorization': auth_header
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers, verify=verify_requests)

    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')

        # Update the cache with the new token and its creation time
        access_token_cache["token"] = token
        access_token_cache["created_at"] = current_time

        return token
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None

def get_spotify_authorization_code(client_id, redirect_uri):
    scope = 'user-read-private user-read-email'
    state = secrets.token_urlsafe(16)  # Optional, but recommended for security

    # Construct the authorization URL
    auth_url = 'https://accounts.spotify.com/authorize?' + \
        f'client_id={client_id}&' + \
        f'response_type=code&' + \
        f'redirect_uri={redirect_uri}&' + \
        f'scope={scope}&' + \
        f'state={state}'
        
    # Open the authorization URL in a web browser for the user to grant permission
    webbrowser.open(auth_url)

def get_spotify_play_state(access_token):
    # Define the Spotify API endpoint
    url = "https://api.spotify.com/v1/me/player"

    # Define the headers with the authorization token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, verify=verify_requests)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract the 'is_playing' value
            is_playing = data.get("is_playing", False)
            return is_playing
        else:
            print(f"Failed to retrieve Spotify play state. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
get_spotify_authorization_code(client_id, redirect_uri)