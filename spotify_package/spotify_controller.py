import threading
from datetime import datetime, timezone
import time

from spotify_package.spotify_api_package.spotify_api_requests import play_music
from spotify_package.spotify_api_package.spotify_tokens_api import get_access_token
from spotify_package.spotify_api_package.spotify_tokens_api import check_access_token

def spotify_play_music(spotify_uri):
    check_access_token()
    access_token = get_access_token()
    play_music(access_token, spotify_uri)

def spotify_choose_uri(event_summary):
    event_summary = event_summary.replace('"', "")
    if(event_summary == 'Gym'):
        print('Playing Gym-Playlist')
        spotify_play_music("spotify:playlist:37i9dQZF1DX6J5NfMJS675")
    elif(event_summary == 'Studying'):
        print('Playing Studying-Playlist')
        spotify_play_music("spotify:playlist:1YIe34rcmLjCYpY9wJoM2p?si=147c2c7749764851")
    elif(event_summary == 'Yoga'):
        print('Playing Yoga-Plalist')
        spotify_play_music("spotify:playlist:37i9dQZF1DX9uKNf5jGX6m")
    else:
        print("Activity needs to be added")


def use_events_for_music(events):
    for event in events:
        event_summary = event.get("summary")
        event_start_time_str = event.get("start", None)

        if event_start_time_str:
            # Convert the event's start time to a datetime object
            event_start_time = datetime.fromisoformat(event_start_time_str[:-1] + "+00:00")

            # Calculate the time until the event starts
            now = datetime.now(timezone.utc)
            test = (event_start_time - now)
            time_until_event = test.total_seconds()

            if time_until_event > 0:
                threading.Timer(time_until_event, spotify_choose_uri, [event_summary]).start()
                #print(f"Waiting for the '{event_summary}' event at {event_start_time}")
                #time.sleep(time_until_event)  # Wait until the event time

                #print(f"Performing action for the '{event_summary}' event")
                #spotify_choose_uri(event_summary)


if __name__ == "__main":
    spotify_play_music("spotify:playlist:37i9dQZF1DX6J5NfMJS675")
