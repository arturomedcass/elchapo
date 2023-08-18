import os
import speech_recognition as sr
import pywhatkit
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

def get_voice_command():
    """Gets a voice command from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Error making the request; {e}")
        return None

def play_song(command):
    song_name = command.replace("play", "")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="a6fec793b2f442faba1302779b8fcbfc",
                                             client_secret="9ac16523ab9d49319a6a9641e53f64c1",
                                             redirect_uri="http://127.0.0.1:9090",
                                             scope = "user-library-read,user-read-playback-state,user-modify-playback-state"))

    results = sp.search(q = song_name, limit=1)
    for idx, track in enumerate(results['tracks']['items']):
        song_id = track['id']
    sp.start_playback(uris=["spotify:track:" + song_id])
    
def give_info(command):
    topic = command.replace("tell me about", "")
    pywhatkit.info(topic)

if __name__ == "__main__":
    command = get_voice_command()
    if command is not None:
        if "play" in command:
            play_song(command)
            pass
        elif "tell me about" in command:
            give_info(command)
            pass
        else:
            print("Unknown command:", command)