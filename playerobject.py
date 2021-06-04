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
        self.old_x = 0
        self.old_y = 0;

        self.kick_mode = False
        self.kick_angle = (0, 0)


    def respawn(self):
        self.x = self.spawnx
        self.y = self.spawny
        self.status = "ALIVE"

        self.tick = 0
        self.anim = 0
        self.is_walking=True
        self.kick_mode = False

    def get_eaten(self):
        self.status = "DEAD"
        self.death_time = time()


    def interact(self, gamestate, release=False):
        if self.status == 'DEAD':
            return

        if not release:
            self.kick_mode = True

            # stop ball
            self.calcKickAngle(gamestate)
            if self.kick_angle != (0, 0):
                gamestate.getBall().stop()

        else: # release
            if self.kick_mode:
                self.kick_mode = False

            if self.kick_angle != (0, 0):
                ball = gamestate.getBall()
                speed = 30
                kickheight = (abs(self.kick_angle[0]) + abs(self.kick_angle[1])) * speed
                ball.kick(self.kick_angle[0] * speed, self.kick_angle[1] * speed, kickheight)

                self.kick_angle = (0, 0)

    def calcKickAngle(self, gamestate):
        ball = gamestate.getBall()

        ballCenterX = ball.x + ball.width/2
        ballCenterY = ball.y + ball.height/2
        playerCenterX = self.x + TILE_W/2
        playerCenterY = self.y + TILE_H - 3
        diffX = ballCenterX - playerCenterX
        diffY = ballCenterY - playerCenterY
        distance = math.sqrt(pow(diffX, 2) + pow(diffY, 2))
        if distance < 16 and distance > 0 and ball.z < 8:
            if VARIABLE_KICK_POWER:
                diffX /= 16
                diffY /= 16
            else:
                diffX /= distance # normalise
                diffY /= distance # normalise

            self.kick_angle = (diffX, diffY)
        else:
            self.kick_angle = (0, 0)


    def update(self, gamestate):

        if self.status == "DEAD":
            if self.death_time + PLAYER_RESPAWN_TIME < time():
                self.respawn()

        speedmod = 0.5 if self.kick_mode else 1

        if REDUCE_DIAGONAL_SPEED:
            if self.xdir != 0 and self.ydir != 0:
                speedmod *= 0.75

        newxdir = self.xdir * self.speed * speedmod
        newydir = self.ydir * self.speed * speedmod

        self.old_x = self.x
        self.old_y = self.y

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
            if colltile1 == "#" or colltile3 == "#":
                newxdir = 0
        elif self.xdir > 0:
            if colltile2 == "#" or colltile4 == "#":
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
            if colltile1 == "#" or colltile2 == "#":
                newydir = 0

        elif self.ydir > 0:
            if colltile3 == "#" or colltile4 == "#":
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

        for currentWorm in gamestate.getWorms():
            if currentWorm._collides_body(self):
                self.x = self.old_x
                self.y = self.old_y

        # check again for EATEN status
        self.status = 'ALIVE'
        for currentWorm in gamestate.getWorms():
            if currentWorm._collides_body(self):
                self.status = 'EATEN'


        # update kick angle
        if self.kick_mode:
            self.calcKickAngle(gamestate)

    def draw(self, screen, tiles, gamestate):

        if self.status == "DEAD":
            return

        if self.status == "EATEN":
            screen.blit(tiles['ea'], (self.x, self.y - TILE_H))
        else:
            screen.blit(tiles[self.tile + str(self.anim)], (self.x, self.y - TILE_H))

        if self.kick_mode and self.kick_angle != (0, 0):
            ball = gamestate.getBall()
            linesize = 16 if VARIABLE_KICK_POWER else 8
            pygame.draw.line(screen, (0, 64, 0), (ball.x + ball.width/2, ball.y + ball.height/2),
                            (ball.x + ball.width/2 + self.kick_angle[0] * linesize, ball.y + ball.height/2 + self.kick_angle[1] * linesize))
