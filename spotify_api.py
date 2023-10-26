import requests
import base64
from constants import Constant

constant = Constant()

client_id = constant.spotify["CLIENT_ID"]
client_secret = constant.spotify["CLIENT_SECRET"]

def get_spotify_access_token(client_id, client_secret):
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

    # Disable SSL certificate verification
    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        return token
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None
    

