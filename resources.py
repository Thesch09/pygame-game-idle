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
    def __init__(self, name, sprite, maxHealth, rarity, purity, size):
        self.name = name
        self.customName = False
        self.sprite = sprite
        self.maxHealth = maxHealth
        self.rarity = rarity
        self.purity = purity # How much of the "mass" is usable. "Mass" is the first value of size multiplied by the other value of size
        self.size = size
        resourceStats.update({self.name:self})
        con.print(f"Created {self.name}, with max health {self.maxHealth}, a rarity of {self.rarity}, a purity of {purity} and a size of {self.size}")


copper = resource("copper", sprites["tempSquare"].sprite, 50, 100, 0.5, (32,32))
iron = resource("iron", sprites["wait"].sprite, 50, 100, 0.05, (32,32))
print(resourceStats)
print(type(resourceStats["copper"]))
def mineResource(plot, resources, ore, miner):
    # plot is there to remove the ore if destroyed:
    ore.health -= miner.damage
    if ore.health <= 0:
        tempOre = ore.name
        tempWorth = math.floor(ore.size[0]*ore.size[1]*ore.purity)
        if tempOre in resources:
            resources.update({tempOre:resources[tempOre]+tempWorth})
        else:
            resources.update({tempOre:tempWorth})
            con.print(f"Added {tempOre} to resources")
        plot.contents.remove(ore)
        con.print(f"removed {ore}")
        plot.reorderContents()
    return resources
def addToPlot(plot, resource):
    class ore:
        # Make the ore
        name = 'copper'
        sprite = None
        health = 0
        purity = 10
        x = 0
        y = 0
        size = (32,32)
        rect = pygame.Rect((x,y),size)
    plot.contents.append(ore)

    plot.contents[-1].health = resource.maxHealth
    plot.contents[-1].purity = resource.purity
    plot.contents[-1].name = resource.name
    plot.contents[-1].size = resource.size
    plot.contents[-1].sprite = resource.sprite

    # Make sure the hitboxes don't overlap
    foundSpot = False
    while not foundSpot:
        plot.contents[-1].x = random.randint(16,496-resource.size[0])
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