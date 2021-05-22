from globalconst import *
from gameobjects import *

class Player(GameObject):
    def __init__(self, x, y, playerid):
        GameObject.__init__(self, x, y)
        self.playerid = playerid

        self.tile = str(playerid)

    def update(self):

        newxdir = self.xdir * self.speed
        newydir = self.ydir * self.speed

        newx = self.x + newxdir
        newy = self.y + newydir

        # collision with screen bounds
        if newx < 0:
            newx = 0
        elif newx > SCR_W - TILE_W:
            newx = SCR_W - TILE_W

        if newy < 0:
            newy = 0
        elif newy > SCR_H - TILE_H*2:
            newy = SCR_H - TILE_H*2

        self.x = newx
        self.y = newy

    def draw(self, screen, tiles):
        screen.blit(tiles[self.tile], (self.x, self.y))
