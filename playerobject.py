import math
from globalconst import *
from gameobjects import *

from time import time

class Player(GameObject):
    def __init__(self, x, y, playerid):
        GameObject.__init__(self, x, y)
        self.playerid = playerid
        self.playertile = playerid % 5 + 1
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


    def interact(self, gamestate):
        ball = gamestate.objects[1]

        ballCenterX = ball.x + ball.width/2
        ballCenterY = ball.y + ball.height/2
        playerCenterX = self.x + TILE_W/2
        playerCenterY = self.y + TILE_H
        diffX = ballCenterX - playerCenterX
        diffY = ballCenterY - playerCenterY + 2
        distance = math.sqrt(pow(diffX, 2) + pow(diffY, 2))
        if distance < 16 and distance > 0:
            speed = 4
            diffX /= distance
            diffY /= distance
            ball.kick(diffX * speed, diffY * speed)


    def update(self, gamestate):

        if self.status == "DEAD":
            if self.death_time+ self.time_to_alive < time():
                self.respawn()

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


        if gamestate.objects[0]._collides_body(self):
            newxdir = 0
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

        if self.status == "DEAD":
            return

        screen.blit(tiles[self.tile + str(self.anim)], (self.x, self.y - TILE_H))