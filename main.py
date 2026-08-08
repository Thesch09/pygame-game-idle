import pygame
from console import con
from imgSetup import setupSprites
from plots import plots
from resources import resourceStats

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

darknors = pygame.Surface((screen.width, screen.height))
darknors.fill((0,0,0))
darknors.set_alpha((0))

clock  = pygame.time.Clock()
deltaTime = 0.1

# Keys
keyEscape = False
quitTimer = 0

# Mouse
mousy = (False, False, False)
mouseState = "Normal"
mouseInteract = "cursor"

# Import sprites
sprites = setupSprites()
activePlot = "Temp"

while Running:
    screen.fill((122,122,122))

    # Hitboxes
    tempHitbox = pygame.Rect((100,100),(16,16))
    pygame.draw.rect(screen, (255,0,0), tempHitbox)
    tempHitbox2 = pygame.Rect((400,100),(16,16))
    pygame.draw.rect(screen, (255,0,0), tempHitbox2)
    mouseHitbox = pygame.Rect((pygame.mouse.get_pos()[0]-3,
                                    pygame.mouse.get_pos()[1]-3),
                                    (6,6))
    pygame.draw.rect(screen, (255,0,0), mouseHitbox)

    collision = tempHitbox.colliderect(mouseHitbox)
    collision2 = tempHitbox2.colliderect(mouseHitbox)
    if collision:
        mouseInteract = "clicker"
    elif collision2:
        mouseInteract = "pickaxe"
    else:
        mouseInteract = "cursor"

    # Rendering of the Plot
    for plot in plots:
        if plot.name == activePlot:
            plot.tickPlot(resourceStats)
            for thing in plot.contents:
                pygame.draw.rect(screen, (255,0,0), thing.rect)
                screen.blit(thing.sprite, (thing.x,thing.y))
                mouseCollision = thing.rect.colliderect(mouseHitbox)
                if mouseCollision:
                    mouseInteract = "pickaxe"

    # Visual unique mouse
    if mousy[0] == True:
        mouseState = "Click"
    else:
        mouseState = "Normal"
    mouse = sprites[f"{mouseInteract}{mouseState}"].sprite
    screen.blit(mouse, (pygame.mouse.get_pos()[0]-mouse.get_width()/2+4,
                        pygame.mouse.get_pos()[1]-mouse.get_height()/2+4))

    # Quitting
    if keyEscape:
        quitTimer += 1 * deltaTime
        darknors.set_alpha(quitTimer*100)
        if quitTimer >= 2:
            Running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                keyEscape = True
                con.print("closing")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                keyEscape = False
                quitTimer = 0
                darknors.set_alpha(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousy = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEBUTTONUP:
            mousy = pygame.mouse.get_pressed()

    screen.blit(darknors)
    pygame.display.flip()

    deltaTime = clock.tick(60) / 1000
    deltaTime = max(0.001, min(0.1, deltaTime))

pygame.quit()