import pygame, math, sys, random

"""Initialization"""
pygame.init()
pygame.font.init()
win = pygame.display.set_mode((500, 500), pygame.RESIZABLE)

"""Game Functions and Classes"""

# Engine classes
class camera(object):
    def __init__(self, initScripts = list[callable], runtimeScripts = list[callable]) -> None:
        self.position = {"x":30, "y":0}
        self.runtimeScripts = runtimeScripts
        for script in initScripts:
            script(self)
    def render(self, renderables) -> None:
        for obj in renderables:
            sclx, scly = obj.sprite.get_size()
            win.blit(obj.sprite, (obj.position["x"] - sclx - self.position["x"], obj.position["y"] - scly + self.position["y"]))
        for script in self.runtimeScripts:
            script(self)

class gameObject(object):
    def __init__(self, position = tuple, sprite = pygame.Surface, rotation = int, initScripts = list[callable], runtimeScripts = list[callable]) -> None:
        self.position = {"x":position[0], "y":position[1]}
        self.rotation = rotation
        self.sprite = sprite
        self.runtimeScripts = runtimeScripts
        for script in initScripts:
            script(self)
    def frame(self) -> None:
        for script in self.runtimeScripts:
            script(self)


class uiType():
    class panel():
        def __init__(self, scale = tuple, position = tuple, color = tuple, textColor = tuple, text = str or None, textPadding = int, font = pygame.font.Font or None, borderRadius = int, initScripts = list[callable], runtimeScripts = list[callable]) -> None:
            # Store runtime scripts and init scripts (this class is only for data storage to make systems more streamlined)
            self.runtimeScripts = runtimeScripts
            self.initScripts = initScripts
            # Store all other data
            self.scale = scale
            self.position = position
            self.color = color
            self.textColor = textColor
            self.text = text
            self.font = font
            self.borderRadius = borderRadius
            self.textPadding = textPadding
            # Store UI type for identification
            self.type = 0
    class button():
        def __init__(self, scale = tuple, position = tuple, color = tuple, hoveredColor = tuple, textColor = tuple, text = str or None, textPadding = tuple, font = pygame.font.Font or None, borderRadius = int, initScripts = list[callable], runtimeScripts = list[callable], onclickScripts = [callable]) -> None:
            # Store runtime scripts and init scripts (this class is only for data storage to make systems more streamlined)
            self.runtimeScripts = runtimeScripts
            self.initScripts = initScripts
            self.onclickScripts = onclickScripts
            # Store all other data
            self.scale = scale
            self.position = position
            self.color = color
            self.textColor = textColor
            self.text = text
            self.font = font
            self.borderRadius = borderRadius
            self.hoveredColor = hoveredColor
            self.textPadding = textPadding
            # Store UI type for identification
            self.type = 1

class uiRenderer(object):
    def __init__(self) -> None:
        return
    def frame(self, renderables) -> None:
        for renderable in renderables:
            if not renderable.hidden:
                win.blit(renderable.sprite, renderable.position)
class uiElement(object):
    def __init__(self, uiData = uiType) -> None:
        # Store and run all scripts
        self.runtimeScripts = uiData.runtimeScripts
        initScripts = uiData.initScripts
        for script in initScripts:
            script(self)
        
        # Store all other data
        self.type = uiData.type
        self.hidden = False
        if self.type in [0,1]: # Check if current uiType supports basic panel parameters
            self.scale = uiData.scale
            self.position = uiData.position
            self.color = uiData.color
            self.text = uiData.text
            self.textColor = uiData.textColor
            self.font = uiData.font
            self.borderRadius = uiData.borderRadius
            self.textPadding = uiData.textPadding
        if self.type in [1]: # Check if current uiType supports basic hover functions
            self.hoveredColor = uiData.hoveredColor
        if self.type == 1: # Check if type is button to allow for click functions
            self.onclickScripts = uiData.onclickScripts

        # Draw sprite
        sprite = pygame.Surface(self.scale, pygame.SRCALPHA)
        pygame.draw.rect(sprite, self.color, (0,0,self.scale[0], self.scale[1]), 0, self.borderRadius)
        text = self.font.render(self.text, True, self.textColor, None, self.scale[0]-self.textPadding[0])
        sprite.blit(text, self.textPadding)
        self.sprite = sprite
        
    def frame(self) -> None:
        for script in self.runtimeScripts:
            script(self)
        if self.type == 1:
            mx, my = pygame.mouse.get_pos()
            if mx > self.position[0] and mx < self.position[0] + self.scale[0] and my > self.position[1] and my < self.position[1] + self.scale[1]:
                sprite = pygame.Surface(self.scale, pygame.SRCALPHA)
                pygame.draw.rect(sprite, self.hoveredColor, (0,0,self.scale[0], self.scale[1]), 0, self.borderRadius)
                text = self.font.render(self.text, True, self.textColor, None, self.scale[0]-self.textPadding[0])
                sprite.blit(text, self.textPadding)
                self.sprite = sprite
                if pygame.mouse.get_pressed()[0]:
                    for script in self.onclickScripts:
                        script(self)
            else:
                sprite = pygame.Surface(self.scale, pygame.SRCALPHA)
                pygame.draw.rect(sprite, (self.color), (0,0,self.scale[0], self.scale[1]), 0, self.borderRadius)
                text = self.font.render(self.text, True, self.textColor, None, self.scale[0]-self.textPadding[0])
                sprite.blit(text, self.textPadding)
                self.sprite = sprite

    def relsprite(self) -> None:
        sprite = pygame.Surface(self.scale, pygame.SRCALPHA)
        pygame.draw.rect(sprite, self.color, (0,0,self.scale[0], self.scale[1]), 0, self.borderRadius)
        text = self.font.render(self.text, True, self.textColor, None, self.scale[0]-self.textPadding[0])
        sprite.blit(text, self.textPadding)
        self.sprite = sprite

class routine(object):
    def __init__(self, scripts = list[callable], frames = int, routineEnd = list[callable]) -> None:
        self.scripts = scripts
        self.totalFrames = frames
        self.routineEndScripts = routineEnd
        self.currentFrame = 0
class routineManager(object):
    def __init__(self) -> None:
        self.routines = []
    def startRoutine(self, scripts = list[callable], frames = int, routineEndScripts = list[callable]) -> None:
        self.routines.append(routine(scripts, frames, routineEndScripts))
    def frame(self):
        for obj in self.routines:
            if obj.currentFrame < obj.totalFrames:
                scripts = obj.scripts
                for script in scripts:
                    script(obj.currentFrame)
                obj.currentFrame += 1
            else:
                self.routines.remove(obj)
                for script in obj.routineEndScripts:
                    script()
        


# Game-Specific functions and classes
def cameraMovement(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        self.position["y"] += 1
    if keys[pygame.K_s]:
        self.position["y"] -= 1
    if keys[pygame.K_d]:
        self.position["x"] += 1
    if keys[pygame.K_a]:
        self.position["x"] -= 1
#def closePasueMenu
    

"""Scene Functions and Main Loop"""

pauseMenuState = 0

def game():
    # Define global variables (Variables )that exist outside of this function)
    global running
    global gameRunning # Define gameRunning globally to allow for other scenes to be accessed other than game

    # Define local variables
    sceneCamera = camera([], [cameraMovement])
    sceneObjects = []

    sceneRoutineManager = routineManager()

    sceneUiRenderer = uiRenderer()
    uiElements = []


    pauseMenu = []

    pauseMenuTip = "Lorem Ipsum"

    pauseMenuTips = [
        "Falling into pits kills you.",
        "Enemies attacking you deals damage.",
        "Dying kills you.",
        "Swimming makes you deplete oxygen.",
        "Walking makes you move.",
        "Jumping makes you jump"
    ]

    idx = 0

    def pauseMenuOpenRoutine(frame):
        global idx
        if idx < len(pauseMenu):
            pauseMenu[idx].position = (-300 + 6.6 * (frame - idx*50), pauseMenu[idx].position[1])
            pauseMenu[idx].hidden = False
            if frame > 50 * (idx+1) - 1:
                idx += 1

    def pauseMenuCloseRoutine(frame):
        global idx
        if idx > -1:
            pauseMenu[idx].position = (-300 - 6.6 * (frame - (len(pauseMenu)-idx)*50), pauseMenu[idx].position[1])
            pauseMenu[idx].hidden = False
            if frame > 50 * (len(pauseMenu)-idx) - 1:
                idx -= 1

    def pauseMenuOpenEnd():
        global pauseMenuState
        pauseMenuState = 2
        print(pauseMenuState)

    def pauseMenuCloseEnd():
        global pauseMenuState
        pauseMenuState = 0
        print(pauseMenuState)

    def openPauseMenu():
        global idx
        global pauseMenuState
        global pauseMenuTip
        pauseMenuTip = random.choice(pauseMenuTips)
        pauseMenu[len(pauseMenu)-1].text = pauseMenuTip
        pauseMenu[len(pauseMenu)-1].relsprite()
        idx = 0
        pauseMenuState = 1
        sceneRoutineManager.startRoutine([pauseMenuOpenRoutine], len(pauseMenu)*50+1, [pauseMenuOpenEnd])

    def closePauseMenu():
        global idx
        global pauseMenuState
        idx = len(pauseMenu) - 1
        sceneRoutineManager.startRoutine([pauseMenuCloseRoutine], len(pauseMenu)*50+1, [pauseMenuCloseEnd])

        pauseMenuState = 1

    def quitgame():
        global gameRunning
        global running
        gameRunning = False
        running = False

    font = pygame.font.Font(None, 30)

    menuFunctions = [["Home", quitgame], ["Settings", quitgame], ["Quit", quitgame]]

    testElem = uiElement(uiType.panel((300, 40), (30, 30), (115, 115, 115), (255, 255, 255), f"Game Paused", (10, 10), font, 10, [], []))
    testElem.hidden = True
    uiElements.append(testElem)
    pauseMenu.append(testElem)

    for x in range(3):
        testElem = uiElement(uiType.button((300, 40), (30, 30+(45*(x+1))), (135, 135, 135), (75, 75, 75), (255, 255, 255), menuFunctions[x][0], (10, 10), font, 5, [], [], [menuFunctions[x][1]]))
        testElem.hidden = True
        uiElements.append(testElem)
        pauseMenu.append(testElem)

    testElem = uiElement(uiType.panel((300, 400), (30, 30+(45*4)), (115, 115, 115), (255, 255, 255), f"Info Panel", (10, 10), font, 10, [], []))
    testElem.hidden = True
    uiElements.append(testElem)
    pauseMenu.append(testElem)

    for x in range(10):
        for y in range(10):
            testSprite = pygame.Surface((50, 50))
            testSprite.fill((0,0,255))
            testObject = gameObject((250 + (x*100), 250 + (y*100)), testSprite, 0, [], [])
            sceneObjects.append(testObject)

    # Game Loop
    while gameRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
                running = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] and pauseMenuState in [0,2]:
                    if pauseMenuState == 0:
                        openPauseMenu()
                        print(pauseMenuState)
                    elif pauseMenuState == 2:
                        closePauseMenu()

        win.fill((255,255,255))

        for obj in sceneObjects:
            obj.frame()
        for elem in uiElements:
            elem.frame()

        sceneRoutineManager.frame()

        # All functions that render to the screen
        sceneCamera.render(sceneObjects)
        sceneUiRenderer.frame(uiElements)

        pygame.display.flip()


running = True
while running:
    gameRunning = True
    game()

# Post runtime logic
pygame.quit()
sys.exit()