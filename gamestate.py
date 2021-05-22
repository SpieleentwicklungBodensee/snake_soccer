import levels

class GameState():
    def __init__(self, levelname='LEV1'):
        self.objects = {}
        self.levelname = levelname
        self.points = 0

    def getLevel(self):
        return levels.levels[self.levelname]
