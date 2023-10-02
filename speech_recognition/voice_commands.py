import os
import speech_recognition as sr
import pywhatkit
from pytube import YouTube
import requests
from moviepy.editor import *
import pyaudio
import pyglet

def get_voice_command():
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
    song_name = command.replace('play ','')
    print("Playing", song_name)
    
    ## Get youtube URL
    url = f"https://www.youtube.com/results?q={song_name}" # Things to fix: remove long videos, movies and live streams
    count = 0
    cont = requests.get(url, timeout=5)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    
    
    ## Download MP4 video
    song_link = f"https://www.youtube.com{lst[count - 5]}" # URL
    try:
        yt = YouTube(song_link)
        song_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    except:
        print("Video is not available")
        play_song(command + " song")
    
    mp4_path = song_stream.download("./songs/")
    
    ## Convert from MP4 to MP3
    mp3_path = mp4_path.replace('mp4', 'mp3')
    song_video = AudioFileClip(mp4_path)
    song_video.write_audiofile(mp3_path)
    os.remove(mp4_path)
    
    ##Play song
    count2 = 0
    for i in range(len(mp3_path)):
        if mp3_path[i] == "/":
            count2 += 1
        if count2 == 1:
            index = i+1
            break
    new_path = mp3_path[index:]
    music = pyglet.resource.media(new_path)
    music.play()
    pyglet.app.run()
    
def give_info(command):
    topic = command.replace("tell me about", "")
    pywhatkit.info(topic)

if __name__ == "__main__":
    command = get_voice_command()
    if command is not None:
        if "play " in command:
            play_song(command)
            pass
        elif "tell me about" in command:
            give_info(command)
            pass
        else:
            print("Unknown command:", command)
