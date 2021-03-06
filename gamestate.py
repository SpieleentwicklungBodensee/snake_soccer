import levels

from worm import Worm
from bird import Bird

class GameState():
    def __init__(self, levelname='LEV1'):
        self.objects = {}
        self.levelname = levelname
        self.points = 0
        self.soundQueue = set()

    def getLevel(self):
        return levels.levels[self.levelname]

    def getWorms(self):
        wormsList = []
        for currentObject in self.objects.values():
            if type(currentObject) is Worm:
                wormsList.append(currentObject)
        return wormsList

    def getBirds(self):
        birdsList = []
        for currentObject in self.objects.values():
            if type(currentObject) is Bird:
                birdsList.append(currentObject)
        return birdsList

    def getBall(self):
        return self.objects[-2]
