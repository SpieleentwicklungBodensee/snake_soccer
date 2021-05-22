import pygame
from globalconst import *
from gameobjects import *

class Ball(GameObject):

    def __init__(self, x, y, tile):

        self.SPEED_DIV = 8*2
        super(Ball, self).__init__(x, y, tile)
        #self.tile = tile
        self.width = 5
        self.height = 4
        #self.x = x
        #self.y = y
        self.z = 0
        self.size = 8
        self.xdir = 10
        self.ydir = 10
        self.zdir = 30

    def kick(self, xdir, ydir):
        if self.z < 8:
            self.xdir = xdir * 5
            self.ydir = ydir * 5
            self.zdir = 20

    def update(self, gamestate):

        # move x
        self.x += self.xdir / self.SPEED_DIV

        # collide x
        hit = False
        if self.x < 0:
            self.x = 0
            hit = True
        if self.x > SCR_W - self.size:
            self.x = SCR_W - self.size
            hit = True

        if hit:
            self.xdir = -self.xdir

        # move y
        self.y += self.ydir / self.SPEED_DIV

        # collide y
        hit = False
        if self.y < 0:
            self.y = 0
            hit = True
        if self.y > SCR_H - self.size:
            self.y = SCR_H - self.size
            hit = True

        if hit:
            self.ydir = -self.ydir

        # move z
        if self.z > 0:
            self.zdir -= 1
        self.z += self.zdir / self.SPEED_DIV

        # collide z
        if self.z < 0:
            self.z = 0
            self.zdir = - self.zdir *2/3
            self.xdir = self.xdir *2/3
            self.ydir = self.ydir *2/3

    def draw(self,screen,tiles):

        shadowColor = (0,96,0)

        # shadow: simple
        #pygame.draw.rect(screen,shadowColor,pygame.Rect(self.x,self.y,self.width,self.height))

        # shadow: size-changing
        shadowShrinkageX=self.z/32
        shadowShrinkageXMax=self.width/2
        if shadowShrinkageX > shadowShrinkageXMax:
            shadowShrinkageX=shadowShrinkageXMax
        shadowShrinkageY=self.z/16
        shadowShrinkageYMax=self.height/2
        if shadowShrinkageY > shadowShrinkageYMax:
            shadowShrinkageY=shadowShrinkageYMax
        pygame.draw.rect(screen,shadowColor,pygame.Rect(self.x+shadowShrinkageX,self.y+1+shadowShrinkageY,self.width-2*shadowShrinkageX,self.height-2*shadowShrinkageY))

        # bounding box at z=0
        if DEBUG_MODE:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x,self.y,self.width,self.height))

        # ball sprite
        screen.blit(tiles[self.tile],(self.x-1,self.y-3-self.z))
