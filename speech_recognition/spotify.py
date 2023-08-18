import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a6fec793b2f442faba1302779b8fcbfc",
                                             client_secret="9ac16523ab9d49319a6a9641e53f64c1",
                                             redirect_uri="http://127.0.0.1:9090",
                                             scope = "user-library-read,user-read-playback-state,user-modify-playback-state"))

def play_song(song_name):
    results = sp.search(q = song_name, limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        song_id = track['id']
    sp.start_playback(uris=["spotify:track:" + song_id])

if __name__ == "__main__":
    song_name = "tetris theme"
    if song_name is not None:
        play_song(song_name)