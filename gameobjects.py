from globalconst import *

class GameObject(object):
    def __init__(self, x, y, tile = None):
        self.x = x
        self.y = y

        self.xdir = 0
        self.ydir = 0
        self.facedir = LEFT

        self.speed = 2
        self.gravity = 2

        self.jump = False
        self.jumpBlocked = False

        self.width = TILE_W
        self.height = TILE_H

        self.tile = None

    def getSprite(self):
        return self.tile

    def moveLeft(self):
        self.xdir = -1

    def moveRight(self):
        self.xdir = 1

    def moveUp(self):
        self.ydir = -1

    def moveDown(self):
        self.ydir = 1

    def doJump(self):
        if not self.jumpBlocked:  # and not self.climb:
            self.ydir = -4
            self.jumpBlocked = True
            self.jump = True

            sfx['jump'].play()

    def stopLeft(self):
        if self.xdir < 0:
            self.xdir = 0

    def stopRight(self):
        if self.xdir > 0:
            self.xdir = 0

    def stopUp(self):
        if self.ydir < 0:
            self.ydir = 0

    def stopDown(self):
        if self.ydir > 0:
            self.ydir = 0

    def cancelJump(self):
        pass

    def update(self):
        pass

    def interact(self):
        pass

    def collides(self, game_object):
        if self.x < game_object.x + game_object.width and \
                self.x + self.width > game_object.x and \
                self.y < game_object.y + game_object.height and \
                self.y + self.height > game_object.y:
            #debugList.append([self.x, self.y])
            #debugList.append([game_object.x, game_object.y])

            return True
        return False