import pygame
from console import con
from imgSetup import setupSprites
from plots import plots
from resources import resourceStats, mineResource

pygame.init()
flags = pygame.FULLSCREEN | pygame.NOFRAME | pygame.SCALED
#flags = pygame.RESIZABLE | pygame.SCALED
screen = pygame.display.set_mode((512,288), flags)
pygame.display.set_caption("test of title")
darkness = 0

Running = True
pygame.mouse.set_visible(False)

tempSquare = pygame.image.load('assets/img/debug/tempSquare.png').convert_alpha()
tempSquare = pygame.transform.scale(tempSquare,
                                    (tempSquare.get_width()*2,
                                     tempSquare.get_height()*2))
pygame.display.set_icon(tempSquare)

# Fonts
regularFont = pygame.font.Font(None, size = 22)

# Modes
darknors = pygame.Surface((screen.width, screen.height))
darknors.fill((0,0,0))
darknors.set_alpha((0))

visualMode = "plotLook"

clock  = pygame.time.Clock()
deltaTime = 0.1

# Keys
pressedKeys = {9:False,13:False,27:False}
quitTimer = 0
stockToggle = False
stockTimer = 0

# Mouse
class makeMouse:
    def __init__(self):
        self.mousy = (False, False, False)
        self.State = "Normal"
        self.Interact = "cursor"
        self.validClick = False
        self.damage = 10
mouse = makeMouse()

# Import sprites
sprites = setupSprites()
activePlot = "Temp"

# The dictonary for saving resources
resources = {}

while Running:
    screen.fill((122,122,122))

    # Hitboxes
    mouseHitbox = pygame.Rect((pygame.mouse.get_pos()[0]-3,
                                        pygame.mouse.get_pos()[1]-3),
                                        (6,6))
    tempHitbox = pygame.Rect((100,100),(16,16))
    tempHitbox2 = pygame.Rect((400,100),(16,16))
    if visualMode == "plotLook":
        pygame.draw.rect(screen, (255,0,0), tempHitbox)
        pygame.draw.rect(screen, (255,0,0), tempHitbox2)
        pygame.draw.rect(screen, (255,0,0), mouseHitbox)

    collision = tempHitbox.colliderect(mouseHitbox)
    collision2 = tempHitbox2.colliderect(mouseHitbox)
    if collision:
        mouse.Interact = "clicker"
    elif collision2:
        mouse.Interact = "pickaxe"
    else:
        mouse.Interact = "cursor"

    # Show ore stats
    if pressedKeys[9]:
        stockTimer += 1*deltaTime
        if stockTimer >= 0.5:
            stockToggle = False

    if pressedKeys[9] and not stockToggle:
        visualMode = "viewStats"
    elif not stockToggle:
        visualMode = "plotLook"

    if visualMode == "viewStats":
        textY = 0
        for ore in resources:
            text = f"{resources[ore]} {ore}"
            visibleFont = regularFont.render(text, True, (0,0,0))
            screen.blit(visibleFont, (32, textY))
            textY += regularFont.get_point_size()
            #con.print(regularFont.get_point_size())

    # Rendering of the Plot
    for plot in plots:
        if plot.name == activePlot:
            plot.tickPlot(resourceStats)
            if visualMode == "plotLook":
                for thing in plot.visualContents:
                    pygame.draw.rect(screen, (255,0,0), thing.rect)
                    screen.blit(thing.sprite, (thing.x,thing.y))
                for thing in plot.contents:
                    mouseCollision = thing.rect.colliderect(mouseHitbox)
                    if mouseCollision:
                        mouse.Interact = "pickaxe"
                        if mouse.mousy[0] and mouse.validClick:
                            print(resources)
                            resources = mineResource(plot, resources, thing, mouse)
                            mouse.validClick = False


    # Visual unique mouse
    if mouse.mousy[0]:
        mouse.State = "Click"
    else:
        mouse.State = "Normal"
    mouseVisual = sprites[f"{mouse.Interact}{mouse.State}"].sprite
    screen.blit(mouseVisual, (pygame.mouse.get_pos()[0]-mouseVisual.get_width()/2+4,
                        pygame.mouse.get_pos()[1]-mouseVisual.get_height()/2+4))

    # Quitting
    if pressedKeys[27]:
        quitTimer += 1 * deltaTime
        darknors.set_alpha(quitTimer*100)
        if quitTimer >= 2:
            Running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            con.print(event.key)
            pressedKeys.update({event.key:True})
            if event.key == pygame.K_ESCAPE:
                con.print("closing")
            if event.key == pygame.K_TAB:
                if stockToggle:
                    stockToggle = False
                    visualMode = "plotLook"
                else:
                    stockToggle = True
                    visualMode = "viewStats"
                
        if event.type == pygame.KEYUP:
            pressedKeys.update({event.key:False})
            if event.key == pygame.K_ESCAPE:
                quitTimer = 0
                darknors.set_alpha(0)
            if event.key == pygame.K_TAB:
                stockTimer = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.mousy = pygame.mouse.get_pressed()
            mouse.validClick = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse.mousy = pygame.mouse.get_pressed()

    screen.blit(darknors)
    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min(0.1, deltaTime))

pygame.quit()