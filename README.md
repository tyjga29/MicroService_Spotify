# MicroService_Spotify
Für DHBW 5. Semester ASE

Dieser MicroService erfüllt zwei Funktionen:
1. Er nimmt Google Calendar Events über MQTT auf
2. Mit gegebenen Authentifikationen ordnet er den Events Playlists zu und spielt diese über Spotify ab

Um den Prozess zu starten und Links abzufangen um sie zu spielen die script.py ausführen.

Um das Abspielen von Spotify zu testen, einfach den spotify_controller als Main ausführen.

Needed libraries:
    requests
    pybase64
    pyyaml
    schedule