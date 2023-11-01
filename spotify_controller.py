import schedule
import asyncio

from spotify_metadata import Spotify_Metadata
from spotify_api_requests import play_music
from spotify_tokens_api import get_access_token
from spotify_tokens_api import check_access_token

async def run_check_viable_access_token():
    while True:
        await asyncio.to_thread(check_access_token)
        await asyncio.sleep(60)  # Run the check every minute

async def main():
    play_music(get_access_token(), "spotify:playlist:37i9dQZF1DX6J5NfMJS675")
    
    # Schedule other tasks if needed

    # Start the check_viable_access_token task
    await asyncio.create_task(run_check_viable_access_token())

if __name__ == '__main__':
    asyncio.run(main())
