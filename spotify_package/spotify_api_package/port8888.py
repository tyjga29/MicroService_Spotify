from flask import Flask, request

app = Flask(__name__)

# This route handles the Spotify callback
@app.route('/callback')
def spotify_callback():
    # Extract the authorization code from the query parameters
    authorization_code = request.args.get('code')
    
    # You can now use the authorization code to obtain an access token from Spotify
    # Implement your token request logic here

    # Example response
    return f'Authorization code: {authorization_code}'

if __name__ == '__main__':
    app.run(host='localhost', port=8888)
