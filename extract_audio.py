from os import listdir, system
from os.path import isfile, join



def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

PATH = "./dir/"
fileList = [shellquote(f[:-4]) for f in listdir(PATH) if (isfile(join(PATH, f)) and f.endswith(".mp4"))]
audioList = [shellquote(f[:-4]) for f in listdir(PATH) if (isfile(join(PATH, f)) and f.endswith(".mp3"))]

for name in fileList:
    if name not in audioList:
        system(f"ffmpeg -loglevel panic -i {PATH + name}.mp4 {PATH + name}.mp3")

