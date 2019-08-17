# uses pygame, eyed3

# imports
import pygame
import sys, json, time, io
from urllib.request import urlopen

# --- Globals ---

WINDOWWIDTH = 640
WINDOWHEIGHT = 480

BORDERCOLOR = (10, 10, 80)
BGCOLOR = (50, 50, 175)
TEXTCOLOR = (255, 255, 255)
TEXTSHADOWCOLOR = (180, 170, 170)
BLANKCOLOR = (212, 226, 238)
LIGHTBLANKCOLOR = (222, 236, 248)
CANVASCOLOR = (150, 150, 160)
BUTTONCOLOR = (100, 100, 200)

# ---         ---

# --- Game Functions ---

def terminate():
    pygame.quit()
    sys.exit()

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('images/sanfrancisco.otf', 12)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Bardicus Pro")

    music = MusicBox()

    songDict = json.loads(open("keywords.json", 'r').read())
    for song in songDict:
        music.queue(song)
    
    mediaBar = box(None, x=WINDOWWIDTH/2, y=WINDOWHEIGHT - 48, w=176, h=48)
    playButton = button(mediaBar["rect"], x=0, y=0, w=32, h=32, image="images/play.png")
    forwardButton = button(mediaBar["rect"], x=56, y=0, w=48, h=32, image="images/forward.png")
    rewindButton = button(mediaBar["rect"], x=-56, y=0, w=48, h=32, image="images/rewind.png")

    displayBox = box(None, x=WINDOWWIDTH/2, y=WINDOWHEIGHT/2, w=WINDOWWIDTH*2/3, h=WINDOWHEIGHT/2)
    
    songImage = image(None, x=displayBox["x"]+15, y=displayBox["y"]+15, image=None)
    
    while True: # start screen loop

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: 
                terminate() # exit game
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                if playButton["rect"].collidepoint(mouse_pos):
                    if playButton["toggle"]:
                        playButton["image"] = pygame.image.load("images/pauseActive.png").convert_alpha()
                    else:
                        playButton["image"] = pygame.image.load("images/playActive.png").convert_alpha()

                if forwardButton["rect"].collidepoint(mouse_pos):
                    forwardButton["image"] = pygame.image.load("images/forwardActive.png").convert_alpha()

                if rewindButton["rect"].collidepoint(mouse_pos):
                    rewindButton["image"] = pygame.image.load("images/rewindActive.png").convert_alpha()
            
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos  # gets mouse position

                if playButton["rect"].collidepoint(mouse_pos):
                    if playButton["toggle"]:
                        playButton["toggle"] = False
                        playButton["image"] = pygame.image.load("images/play.png").convert_alpha()
                        music.pause()
                        
                    else:
                        playButton["toggle"] = True
                        playButton["image"] = pygame.image.load("images/pause.png").convert_alpha()
                        if not music.song: 
                            music.next()
                            songImage = updateImage(songImage, io.BytesIO(urlopen(f"https://i.ytimg.com/vi/{music.song}/default.jpg").read()))
                        else: music.resume()
                        
                if forwardButton["rect"].collidepoint(mouse_pos):
                    forwardButton["image"] = pygame.image.load("images/forward.png").convert_alpha()
                    playButton["toggle"] = True
                    playButton["image"] = pygame.image.load("images/pause.png").convert_alpha()
                    music.next()
                    songImage = updateImage(songImage, io.BytesIO(urlopen(f"https://i.ytimg.com/vi/{music.song}/default.jpg").read()))
                
                if rewindButton["rect"].collidepoint(mouse_pos):
                    rewindButton["image"] = pygame.image.load("images/rewind.png").convert_alpha()
                    playButton["toggle"] = True
                    playButton["image"] = pygame.image.load("images/pause.png").convert_alpha()
                    music.restart()
        
        # Render:
        DISPLAYSURF.fill(BGCOLOR)
        pygame.draw.rect(DISPLAYSURF, CANVASCOLOR, mediaBar["rect"])
        renderButton(playButton)
        renderButton(forwardButton)
        renderButton(rewindButton)
        drawText(music.song, BASICFONT, (0, 0))
        pygame.draw.rect(DISPLAYSURF, CANVASCOLOR, displayBox["rect"])
        if music.song: renderImage(songImage)
        if music.song: drawText(f"{songDict[music.song]['title']}", BASICFONT, (songImage["x"], songImage["y"]+100))
        if music.song: drawText(f"{songDict[music.song]['description']}", BASICFONT, (songImage["x"], songImage["y"]+120))
        pygame.display.flip()
        
        FPSCLOCK.tick()

def box(parentRect, x, y, w, h):
    boxDict = {"w": w, "h": h}
    boxDict["x"] = x + (parentRect.center[0] if parentRect else 0) - boxDict["w"] / 2
    boxDict["y"] = y + (parentRect.center[1] if parentRect else 0) - boxDict["h"] / 2 
    boxDict["rect"] = pygame.Rect((boxDict["x"], boxDict["y"], boxDict["w"], boxDict["h"]))
    return boxDict

def image(parentRect, x, y, image):
    imageDict = {"x": x + (parentRect.center[0] if parentRect else 0), "y": y + (parentRect.center[1] if parentRect else 0)}
    imageDict["image"] = pygame.image.load(image).convert_alpha() if image else None
    return imageDict

def updateImage(imageDict, image):
    imageDict["image"] = pygame.image.load(image).convert_alpha()
    return imageDict

def button(parentRect, x, y, w, h, image=None):
    buttonDict = {"w": w, "h": h, "toggle": False, "active": False}
    buttonDict["x"] = x + (parentRect.center[0] if parentRect else 0) - buttonDict["w"] / 2
    buttonDict["y"] = y + (parentRect.center[1] if parentRect else 0) - buttonDict["h"] / 2 
    buttonDict["rect"] = pygame.Rect((buttonDict["x"], buttonDict["y"], buttonDict["w"], buttonDict["h"]))
    if image: buttonDict["image"] = pygame.image.load(image).convert_alpha()
    return buttonDict

def renderImage(image):
    #pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, button["rect"])  # draw button
    DISPLAYSURF.blit(image["image"], (image["x"], image["y"])) # paint to screen

def renderButton(button):
    #pygame.draw.rect(DISPLAYSURF, BUTTONCOLOR, button["rect"])  # draw button
    DISPLAYSURF.blit(button["image"], (button["x"], button["y"])) # paint to screen

def drawText(text, font, location, color=None, center=False):
    textSurf = font.render(text, True, color if color else TEXTCOLOR)
    textRect = textSurf.get_rect()
    if center: textRect.center = location
    else: textRect.topleft = location
    DISPLAYSURF.blit(textSurf, textRect)

class MusicBox():

    def __init__(self):
        self.song = None
        self.q = []

    def queue(self, song):
        self.q.append(song)
        return True

    def restart(self):
        if self.song: self.stop(delete=False)
        if len(self.q):
            self.song = self.q[0]
        else:
            return False
        musicFile = f"music/{self.song}.mp3"
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(0)
        return True

    def next(self):
        if self.song: self.stop()
        if len(self.q):
            self.song = self.q[0]
        else:
            return False
        musicFile = f"music/{self.song}.mp3"
        pygame.mixer.music.load(musicFile)
        pygame.mixer.music.play(0)
        return True

    def stop(self, delete=True):
        self.song = None
        if delete: del self.q[0]
        pygame.mixer.fadeout(1)
        pygame.mixer.music.stop()
        return True

    def pause(self):
        pygame.mixer.fadeout(1)
        pygame.mixer.music.pause()
        return True

    def resume(self):
        pygame.mixer.music.unpause()
        return True


if __name__ == "__main__":
    main()
