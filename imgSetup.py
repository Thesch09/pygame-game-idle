import pygame
import os

screen = pygame.display.set_mode((512,288))
class makeSprites:
    def __init__(self, sprite):
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite,
                                    (self.sprite.get_width()*2,
                                     self.sprite.get_height()*2))

def setupSprites():
    sprites = {}
    subFolders = os.listdir("assets/img")
    for folder in subFolders:
        images = os.listdir(f"assets/img/{folder}")
        print(f"looking in folder {folder}")
        for sprite in images:
            sprites.update({sprite.split(".png")[0]:makeSprites(f"assets/img/{folder}/{sprite}")})
    print(sprites)
    return sprites