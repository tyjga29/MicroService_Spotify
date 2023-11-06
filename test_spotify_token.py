import unittest
from unittest.mock import patch

from datetime import datetime, timedelta

from spotify_package.spotify_api_package.spotify_tokens_api import check_access_token 

class TestCheckAccessToken(unittest.TestCase):
    @patch('spotify_package.spotify_api.spotify_tokens_api.check_access_token')
    def test_refresh_token_calles(self, mock_refresh_token):
        access_token_cache = {
            "access_token": 'Valid Token',
            "refresh_token": 'Valid Token',
            "expires_at": datetime.now() - timedelta(seconds=60)
        }
    
        mock_refresh_token.return_value = 'new_access_token'
        check_access_token()
        mock_refresh_token.assert_called_with(client_id, client_secret, access_token_cache['refresh_token'])
        self.assertEqual(access_token_cache['access_token'], 'new_access_token')


    

if __name__ == '__main__':
    unittest.main()
