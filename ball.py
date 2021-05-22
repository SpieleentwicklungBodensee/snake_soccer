import pygame
from globalconst import *
from gameobjects import *

class Ball(GameObject):
    def __init__(self, x, y, tile = None):
        super(Ball, self).__init__(x, y, tile)
        #self.x = x
        #self.y = y
        self.z = 20
        #self.tile = tile

        self.size = 8
        self.xdir = 10
        self.ydir = 10
        self.zdir = 0

        self.SPEED_DIV = 8

    def update(self):

        # move x
        self.x += self.xdir / self.SPEED_DIV

        # collide x
        if self.x < 0:
            self.x = 0
            self.xdir = -self.xdir
        if self.x > SCR_W - self.size:
            self.x = SCR_W - self.size
            self.xdir = -self.xdir

        # move y
        self.y += self.ydir / self.SPEED_DIV

        # collide y
        if self.y < 0:
            self.y = 0
            self.ydir = -self.ydir
        if self.y > SCR_H - self.size:
            self.y = SCR_H - self.size
            self.ydir = -self.ydir

        # move z
        if self.z > 0:
            self.zdir -= 1
        self.z += self.zdir / self.SPEED_DIV
        if self.z < 0:
            self.z = 0
            self.zdir = - self.zdir 


    def draw(self,screen,tiles):
        # shadow
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.x,self.y,self.size,self.size))
        # bounding box
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x,self.y-self.z,self.size,self.size))
        # sprite
        screen.blit(tiles[self.tile],(self.x,self.y-self.z))
