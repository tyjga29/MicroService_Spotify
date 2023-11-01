import requests

def error_response(response):
    print(f"Error: {response.status_code}")
    print(response.text)
    return None  # Handle the error as needed

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
        
    
