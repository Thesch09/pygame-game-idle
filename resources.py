import pygame
import random
import math
import time
from imgSetup import setupSprites
from console import con

screen = pygame.display.set_mode((512,288))

resourceStats = {}

sprites = setupSprites()

class resource:
    def __init__(self, name, sprite, maxHealth, rarity, value, size):
        self.name = name
        self.customName = False
        self.sprite = sprite
        self.maxHealth = maxHealth
        self.rarity = rarity
        self.value = value
        self.size = size
        resourceStats.update({self.name:self})
        con.print(f"Created {self.name}, with max health {self.maxHealth}, a rarity of {self.rarity}, a value of {value} and a size of {self.size}")


copper = resource("copper", sprites["tempSquare"].sprite, 80, 100, 10, (32,32))
print(resourceStats)
print(type(resourceStats["copper"]))
def addToPlot(plot, resource):
    class ore:
        # Make the ore
        name = 'copper'
        sprite = None
        maxHealth = 80
        health = 0
        value = 10
        damage = 0
        x = 0
        y = 0
        size = (32,32)
        rect = pygame.Rect((x,y),size)
    plot.contents.append(ore)

    plot.contents[-1].size = resource.size
    plot.contents[-1].sprite = resource.sprite

    # Make sure the hitboxes don't overlap
    foundSpot = False
    while not foundSpot:
        plot.contents[-1].x = random.randint(16,496)
        plot.contents[-1].y = random.randint(16,224)
        
        plot.contents[-1].rect = pygame.Rect((plot.contents[-1].x, plot.contents[-1].y),plot.contents[-1].size)
        if len(plot.contents) == 0:
            # This is the first thing in the list
            con.print("Nothing else to take space")
            break
        for item in plot.contents:
            # Check everything else in the list. If it collides with something, pick a new spot
            collision = plot.contents[-1].rect.colliderect(item.rect)
            if collision and item != plot.contents[-1]:
                con.print("No spot")
                break
        else:
            # It hasn't collided with anything, so it can be placed
            foundSpot = True
            con.print("PLACED")
    
    # Setting the item in the correct spot in the list for a 3D effect
    '''for item in plot.contents:
        if item[-1].y < resource.y:
            plot.contents.append("item")
            print("Added")
            return plot.contents'''