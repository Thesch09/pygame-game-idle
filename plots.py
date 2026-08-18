import pygame
import random
import math
from console import con
from resources import resourceStats, addToPlot

screen = pygame.display.set_mode((512,288))

plots = []

class plot:
    def __init__(self, name = str, type = str, pool = dict):
        global plots
        self.name = name
        self.type = type
        self.pool = pool
        self.contents = []
        self.visualContents = [] # Contents but sorted
        self.maxStuff = 5
        self.maxWorkers = 3
        self.workers = 0
        con.print(f"Created new plot {self.name} of type {self.type} with items {self.pool}")
        plots.append(self)
    def tickPlot(self, resources):
        if len(self.contents) < self.maxStuff:
            if random.randint(1,20+len(self.contents)) == 1:
                for item in self.pool:
                    if random.randint(self.pool[item], 100) == 100:
                        addToPlot(self,resources[item])
                        self.reorderContents()
                        
                        con.print(f"Added {item} to {self.name}")
                        break
                else:
                    con.print("[red]Failed generation")
    def reorderContents(self):
        tempList = []

        # Add a list containing Y position and the thing to a list, sort that list, put the item back into the contents list
        for item in self.contents:
            number = 0
            for thing in tempList:
                if thing[0] == item.y:
                    number += 1
            tempList.append([item.y, number,item])
        try:
            tempList.sort()
        except TypeError:
            con.print(f"{tempList} huh")
            return
        self.visualContents = []
        for item in tempList:
            self.visualContents.append(item[2])

tempPlot = plot("Temp", "wildzone", {"copper":50,"iron":50})
print(plots[0].name)