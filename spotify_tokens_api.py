import requests
import base64
import time
import webbrowser
import secrets
import yaml

from datetime import datetime, timedelta

from constants import Constant

# Worklflow of the Tokens
# When a new scope is needed you can add it to the request_scope variable
# run port8888.py to listen to the redirect uri
# Run _private_get_spotify_authorization_code: A browser window will open and the user has to give permission to the scopes
# You will be redirected to the redirect_uri where the authorization code is displayed
# Replace the code in the resource.yaml file and run _private_get_personal_spotify_access_token
# The Access Token, Replicate Token and the new expiration time will be printed
# Replace them in the resource.yaml
# When needed (One hour after the creation of the Access Token), run refresh_spotify_access_token, variables in the yaml will be replaced

#TODO set when ready to true
verify_requests = False

constant = Constant()

client_id = constant.spotify["CLIENT_ID"]
client_secret = constant.spotify["CLIENT_SECRET"]
redirect_uri = constant.spotify["REDIRECT_URI"]
authorization_code = constant.spotify["AUTHORIZATION_CODE"]

# Cache for storing the access token and its creation time
access_token_cache = {
    "access_token": constant.spotify["ACCESS_TOKEN"],
    "refresh_token": constant.spotify["REFRESH_TOKEN"],
    "expires_at": constant.spotify["EXPIRES_AT"]
}

request_scope = 'user-read-private user-read-email user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control'

def _private_get_spotify_access_token(client_id, client_secret):
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

def _private_get_spotify_authorization_code(client_id, redirect_uri):
    scope = request_scope
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
    
def _private_get_personal_spotify_access_token(client_id, client_secret, authorization_code, redirect_uri):
    # Encode the client ID and client secret in Base64 format for the Authorization header
    base64_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')

    # Define the token request parameters
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri
    }

    # Define the headers for the POST request
    token_headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Send the POST request to obtain the access token
    response = requests.post(token_url, data=token_data, headers=token_headers)

    if response.status_code == 200:
        # Parse the JSON response
        token_info = response.json()

        # Access the access token and other information
        access_token = token_info['access_token']
        refresh_token = token_info['refresh_token']
        current_time = datetime.now()
        expires_in = token_info['expires_in']
        expires_at = current_time + timedelta(seconds=expires_in)

        print("Access Token: ", access_token)
        print("Refresh Token ", refresh_token)
        print("Expires_at ", expires_at)
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

def _private_refresh_spotify_access_token(client_id, client_secret, refresh_token):
    # Define the token request parameters
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    # Encode the client ID and client secret in Base64 format for the Authorization header
    base64_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')

    # Define the headers for the POST request
    token_headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Send the POST request to refresh the access token
    response = requests.post(token_url, data=token_data, headers=token_headers)

    if response.status_code == 200:
        # Parse the JSON response
        token_info = response.json()

        # Access the access token and other information
        new_access_token = token_info['access_token']
        current_time = datetime.now()
        expires_in = token_info['expires_in']
        new_expires_at = current_time + timedelta(seconds=expires_in)

        #Overwrite the yaml file with the new variables
        # Load the existing YAML data from the file
        with open('resource.yaml', 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        data['spotify_api_access_data']['ACCESS_TOKEN'] = new_access_token
        data['spotify_api_access_data']['EXPIRES_AT'] = new_expires_at

        with open('resource.yaml', 'w') as file:
            yaml.dump(data, file)

        access_token_cache['access_token'] = new_access_token
        access_token_cache['expires_at'] = new_expires_at
        return new_access_token

    else:
        print(f'Error: {response.status_code}')
        print(response.text)

def _private_print_accesstoken():
    print('Access Token: ', access_token_cache['access_token'], ' Refresh Token: ', access_token_cache['refresh_token'], 'Expires at: ', access_token_cache['expires_at'])

def get_viable_access_token():
    if(access_token_cache['expires_at'] <= datetime.now()):
        access_token = _private_refresh_spotify_access_token(client_id, client_secret, access_token_cache['refresh_token'])
        return access_token