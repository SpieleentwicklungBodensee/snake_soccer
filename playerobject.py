from globalconst import *
from gameobjects import *

class Player(GameObject):
    def __init__(self, x, y, playerid):
        GameObject.__init__(self, x, y)
        self.playerid = playerid
        self.playertile = playerid % 3 + 1
        self.tile = str(self.playertile)
        self.tick = 0
        self.anim = 0
        self.is_walking = True

    def update(self, gamestate):
        newxdir = self.xdir * self.speed
        newydir = self.ydir * self.speed

        newx = self.x + newxdir
        newy = self.y + newydir

        x1 = int(newx / TILE_W)
        x2 = int((newx + TILE_W - 1) / TILE_W)
        y1 = int(newy / TILE_H)
        y2 = int((newy + TILE_H - 1) / TILE_H)

        colltile1 = gamestate.getLevel()[y1][x1]  # upper left
        colltile2 = gamestate.getLevel()[y1][x2]  # upper right
        colltile3 = gamestate.getLevel()[y2][x1]  # lower left
        colltile4 = gamestate.getLevel()[y2][x2]  # lower right

        if self.xdir < 0:
            if colltile1 != " " or colltile3 != " ":
                newxdir = 0
        elif self.xdir > 0:
            if colltile2 != " " or colltile4 != " ":
                newxdir = 0

        newx = self.x
        newy = self.y + newydir

        x1 = int(newx / TILE_W)
        x2 = int((newx + TILE_W - 1) / TILE_W)
        y1 = int(newy / TILE_H)
        y2 = int((newy + TILE_H - 1) / TILE_H)

        colltile1 = gamestate.getLevel()[y1][x1]  # upper left
        colltile2 = gamestate.getLevel()[y1][x2]  # upper right
        colltile3 = gamestate.getLevel()[y2][x1]  # lower left
        colltile4 = gamestate.getLevel()[y2][x2]  # lower right

        if self.ydir < 0:
            if colltile1 != " " or colltile2 != " ":
                newydir = 0

        elif self.ydir > 0:
            if colltile3 != " " or colltile4 != " ":
                newydir = 0

        newx = self.x + newxdir
        newy = self.y + newydir

        self.tick += 1

        if self.is_walking:
            if self.tick % 20 > 10:
                self.anim = 2
            else:
                self.anim = 1
        else:
            self.anim = 0

        # collision with screen bounds
        if newx < 0:
            newx = 0
        elif newx > SCR_W - TILE_W:
            newx = SCR_W - TILE_W

        if newy < 0:
            newy = 0
        elif newy > SCR_H - TILE_H*2:
            newy = SCR_H - TILE_H*2

        self.is_walking = (self.xdir != 0) or (self.ydir != 0)

        self.x = newx
        self.y = newy

    def draw(self, screen, tiles):
        screen.blit(tiles[self.tile + str(self.anim)], (self.x, self.y-TILE_H))
