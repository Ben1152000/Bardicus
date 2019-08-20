# pip3 installed mps-youtube

import os
from pytube import YouTube

URL = "https://www.youtube.com/watch?v={}"
SHORT_URL = "https://youtu.be/{}"
PATH = "./music/"
KEYWORDS = "keywords.json"

def ask(query):
    answer = None
    while answer not in ("yes", "no"):
        answer = input(query)
        if answer == "yes" or answer == 'y': return True
        elif answer == "no" or answer == 'n': return False
        else: print("Please enter yes or no.")

def downloadVideo(videourl, path, filename):
    yt = YouTube(videourl)
    data = {"title": yt.title, "description": yt.description, "length": yt.length}
    title = f"{filename} ({int(yt.length) // 60}:{(int(yt.length) % 60):02d}) - {yt.title}"
    description = f"\n\t{yt.description[:100]}{'...' if len(yt.description) > 100 else ''}"
    print(f"{title}{description if len(description.strip()) > 0 else ''}")
    if (int(yt.length) < 600 or ask(f"\tVideo length is over 10 minutes, are you sure you want to download? ")):
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if not os.path.exists(path):
            os.makedirs(path)
        yt.download(path, filename=filename)
        return data

# downloads a youtube video to a file located in PATH
def download(code):
    code = code.strip()
    if (not len(code) == 11):
        print(f"Invalid Youtube Code: <{code}>"); return
    if (not os.path.isfile(f"{PATH}{code}.mp3")):
        data = downloadVideo(SHORT_URL.format(code), PATH, code)
        os.system(f"ffmpeg -n -loglevel panic -i {PATH}{code}.mp4 {PATH}{code}.mp3")
        if os.path.exists(f"{PATH}{code}.mp4"): os.remove(f"{PATH}{code}.mp4")
        return data

import json

with open(KEYWORDS) as keywordsFile:
    keywords = json.loads(keywordsFile.read())
    for code in keywords:
        if (len(code.strip()) > 0):
            data = download(code.strip())
            if data != None:
                keywords[code] = (data)
                if "keywords" not in keywords[code]:
                    keywords[code]["keywords"] = []
    json.dump(keywords, open(KEYWORDS, 'w'), indent=3)
