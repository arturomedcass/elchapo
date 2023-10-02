import os
import pywhatkit
from pytube import YouTube
import requests
from moviepy.editor import *
import pyaudio
import pyglet

def play_song(command):
    song_name = command.replace('play','')
    print("Playing", song_name)
    
    ## Get youtube URL
    url = f"https://www.youtube.com/results?q={song_name}"
    count = 0
    cont = requests.get(url, timeout=5)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count += 1
        if i == "WEB_PAGE_TYPE_WATCH":
            break
    '''
    with open('video_data.txt', 'w') as f:
        for i in range(0, len(lst)):
            f.write(lst[i])
    '''
    if lst[count - 5] == "/results":
        raise Exception("No Video Found for this Topic!")
    song_link = f"https://www.youtube.com{lst[count - 5]}" # URL
    
    ## Download MP4 video
    yt = YouTube(song_link)
    song_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    mp4_path = song_stream.download("./songs/")
    mp3_path = mp4_path.replace('mp4', 'mp3')
    
    ## Convert from MP4 to MP3
    song_video = AudioFileClip(mp4_path)
    song_video.write_audiofile(mp3_path)
    os.remove(mp4_path)
    
    ##Play song
    count = 0
    for i in range(len(mp3_path)):
        if mp3_path[i] == "/":
            count += 1
        if count == 1:
            index = i+1
            break
    new_path = mp3_path[index:]
    music = pyglet.resource.media(new_path)
    music.play()
    pyglet.app.run()
    
if __name__ == "__main__":
    command = "play tetris song"
    if command is not None:
        if "play" in command:
            play_song(command)
            pass