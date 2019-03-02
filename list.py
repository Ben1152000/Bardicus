
import download

with open("list.txt") as listFile:
    line = listFile.readline()
    while (line):
        if (len(line.strip()) > 0):
            download.download(line.strip())
        line = listFile.readline()