import levels

from worm import Worm

class GameState():
    def __init__(self, levelname='LEV1'):
        self.objects = {}
        self.levelname = levelname
        self.points = 0

    def getLevel(self):
        return levels.levels[self.levelname]

    def getWorms(self):
        wormsList = []
        for currentObject in self.objects.values():
            if type(currentObject) == Worm:
                wormsList.append(currentObject)
        return wormsList

    def getBall(self):
        return self.objects[-2]
