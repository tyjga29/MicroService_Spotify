import requests
import base64

client_id = 'd6caaa509afd447d8344c155bc310e55'
client_secret = '9174d1a1214f438dada61c1b7d7cb1bd'

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
    print(f'Access Token: {token}')
else:
    print(f'Error: {response.status_code}')
    print(response.text)
