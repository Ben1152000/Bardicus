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

    def loop(self):
        pass

    def update(self):
        print(self.q)

class Box():

    def __init__(self, parent, x, y, w, h):
        self.parent = parent
        if self.parent == None: self.rect = pygame.Rect((x, y, w, h))
        else: self.rect = pygame.Rect((x + parent.rect.x, y + parent.rect.y, w, h))
        self.color = CANVASCOLOR
        self.borderColor = None
    
    def setColor(self, color):
        self.color = color
    
    def getColor(self):
        return self.color

    def setBorderColor(self, color):
        self.borderColor = color
    
    def getBorderColor(self):
        return self.borderColor

    def render(self):
        if self.borderColor != None:
            borderRect = pygame.Rect((self.rect.x + 2, self.rect.y + 2, self.rect.w - 4, self.rect.h - 4))
            pygame.draw.rect(DISPLAYSURF, self.borderColor, self.rect)
            pygame.draw.rect(DISPLAYSURF, self.color, borderRect)
        else:
            pygame.draw.rect(DISPLAYSURF, CANVASCOLOR, self.rect)

class Button(Box):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.toggled = False
        self.active = False
    
    def click(self, location):
        if self.rect.collidepoint(location):
            self.active = True
            self.doWhenClicked()

    def doWhenClicked(self):
        print("Clicked!")

    def release(self, location=None):
        if location == None or (self.rect.collidepoint(location) and self.active):
            self.active = False
            self.toggled = not self.toggled
            self.doWhenReleased()
        else:
            self.active = False
            self.doWhenCancelled()
        
    def doWhenReleased(self):
        print("Released!")

    def doWhenCancelled(self):
        print("Cancelled!")
    
    def render(self):
        DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y)) # paint to screen

class PlayButton(Button):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.inactiveImage = pygame.image.load("images/play.png").convert_alpha()
        self.activeImage = pygame.image.load("images/playActive.png").convert_alpha()
        self.toggledInactiveImage = pygame.image.load("images/pause.png").convert_alpha()
        self.toggledActiveImage = pygame.image.load("images/pauseActive.png").convert_alpha()
        
        self.image = self.inactiveImage
    
    def doWhenClicked(self):
        if self.toggled: 
            self.image = self.toggledActiveImage
        else: 
            self.image = self.activeImage

    def doWhenReleased(self):
        if self.toggled: 
            self.image = self.toggledInactiveImage
            if not MUSICBOX.song:
                MUSICBOX.next()
                #SONGIMAGE = updateImage(SONGIMAGE, io.BytesIO(urlopen(f"https://i.ytimg.com/vi/{MUSICBOX.song}/default.jpg").read()))
            else: MUSICBOX.resume()
        else:
            self.image = self.inactiveImage
            MUSICBOX.pause()
    
    def doWhenCancelled(self):
        if self.toggled: 
            self.image = self.toggledInactiveImage
        else: 
            self.image = self.inactiveImage

class ForwardButton(Button):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.inactiveImage = pygame.image.load("images/skip.png").convert_alpha()
        self.activeImage = pygame.image.load("images/skipActive.png").convert_alpha()
        self.image = self.inactiveImage
    
    def doWhenClicked(self):
        self.image = self.activeImage

    def doWhenReleased(self):
        self.image = self.inactiveImage
        if not playButton.toggled: playButton.release()
        MUSICBOX.next()
        #SONGIMAGE = updateImage(SONGIMAGE, io.BytesIO(urlopen(f"https://i.ytimg.com/vi/{MUSICBOX.song}/default.jpg").read()))

    def doWhenCancelled(self):
        self.image = self.inactiveImage

class RewindButton(Button):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.inactiveImage = pygame.image.load("images/back.png").convert_alpha()
        self.activeImage = pygame.image.load("images/backActive.png").convert_alpha()
        self.image = self.inactiveImage
    
    def doWhenClicked(self):
        self.image = self.activeImage

    def doWhenReleased(self):
        self.image = self.inactiveImage
        if not playButton.toggled: playButton.release()
        MUSICBOX.restart()

    def doWhenCancelled(self):
        self.image = self.inactiveImage

class LoopButton(Button):

    def __init__(self, parent, x, y, w, h):
        super().__init__(parent, x, y, w, h)
        self.inactiveImage = pygame.image.load("images/loop.png").convert_alpha()
        self.activeImage = pygame.image.load("images/loopActive.png").convert_alpha()
        self.toggledInactiveImage = pygame.image.load("images/noloop.png").convert_alpha()
        self.toggledActiveImage = pygame.image.load("images/noloopActive.png").convert_alpha()
        self.image = self.inactiveImage
    
    def doWhenClicked(self):
        if self.toggled: 
            self.image = self.toggledActiveImage
        else: 
            self.image = self.activeImage

    def doWhenReleased(self):
        if self.toggled: 
            self.image = self.toggledInactiveImage
        else:
            self.image = self.inactiveImage

    def doWhenCancelled(self):
        self.image = self.inactiveImage

class Image(Box):

    def __init__(self, parent, x, y, image):
        super().__init__(parent, x, y, w, h)
        self.image = image
    
    def setImage(self, image):
        self.image = image

    def render(self):
        DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y)) # paint to screen


def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT, MUSICBOX
    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()
    BASICFONT = pygame.font.Font('images/sanfrancisco.otf', 12)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    MUSICBOX = MusicBox()
    pygame.display.set_caption("Bardicus Pro")

    songDict = json.loads(open("keywords.json", 'r').read())
    for song in songDict:
        MUSICBOX.queue(song)
    
    global playButton, forwardButton, rewindButton
    mediaBar = Box(None, x=WINDOWWIDTH/2-88, y=WINDOWHEIGHT-72, w=176, h=48)
    mediaBar.setBorderColor(BORDERCOLOR)
    rewindButton = RewindButton(parent=mediaBar, x=8, y=8, w=40, h=32)
    playButton = PlayButton(parent=mediaBar, x=50, y=8, w=32, h=32)
    forwardButton = ForwardButton(parent=mediaBar, x=92, y=8, w=40, h=32)
    loopButton = LoopButton(parent=mediaBar, x=136, y=8, w=32, h=32)

    displayBox = Box(None, x=WINDOWWIDTH/6, y=WINDOWHEIGHT/4, w=WINDOWWIDTH*2/3, h=WINDOWHEIGHT/2)

    while True: # start screen loop

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                terminate() # exit game
            if event.type == pygame.MOUSEBUTTONDOWN:
                playButton.click(event.pos)
                forwardButton.click(event.pos)
                rewindButton.click(event.pos)
                loopButton.click(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                playButton.release(event.pos)
                forwardButton.release(event.pos)
                rewindButton.release(event.pos)
                loopButton.release(event.pos)
        
        # Render:
        DISPLAYSURF.fill(BGCOLOR)
        mediaBar.render()
        playButton.render()
        forwardButton.render()
        rewindButton.render()
        loopButton.render()
        drawText(MUSICBOX.song, BASICFONT, (0, 0))
        displayBox.render()
        if MUSICBOX.song: drawText(f"{songDict[MUSICBOX.song]['title']}", BASICFONT, (120, 150))
        if MUSICBOX.song: drawText(f"{songDict[MUSICBOX.song]['description']}", BASICFONT, (120, 180))
        pygame.display.flip()
        FPSCLOCK.tick()

def drawText(text, font, location, color=None, center=False):
    textSurf = font.render(text, True, color if color else TEXTCOLOR)
    textRect = textSurf.get_rect()
    if center: textRect.center = location
    else: textRect.topleft = location
    DISPLAYSURF.blit(textSurf, textRect)

if __name__ == "__main__":
    main()
