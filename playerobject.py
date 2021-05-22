from globalconst import *
from gameobjects import *

from time import time

class Player(GameObject):
    def __init__(self, x, y, playerid):
        GameObject.__init__(self, x, y)
        self.playerid = playerid
        self.playertile = playerid % 3 + 1
        self.tile = str(self.playertile)
        self.tick = 0
        self.anim = 0
        self.is_walking = True

        self.status = "ALIVE"
        self.death_time    =0
        self.time_to_alive = 2



    def respawn(self):
        self.x =TILE_W * 2
        self.y =TILE_H * 2
        self.status = "ALIVE"

        self.tick = 0
        self.anim = 0
        self.is_walking=True

    def get_eaten(self):
        self.status = "DEAD"
        self.death_time = time()



    def update(self, gamestate):

        if self.status == "DEAD":
            if self.death_time+ self.time_to_alive < time():
                self.respawn()

        newxdir = self.xdir * self.speed
        newydir = self.ydir * self.speed

        newx = self.x + newxdir
        newy = self.y + newydir

        self.is_walking = (self.xdir != 0) or (self.ydir != 0)

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

        self.x = newx
        self.y = newy

    def draw(self, screen, tiles):

        if self.status == "DEAD":
            return

        screen.blit(tiles[self.tile + str(self.anim)], (self.x, self.y- self.height))