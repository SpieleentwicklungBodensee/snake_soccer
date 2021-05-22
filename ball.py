import pygame
import gameobjects
from globalconst import *
from time import time

class Ball(gameobjects.GameObject):
    def __init__(self,x,y,tile_w,tile_h):
        super(Ball, self).__init__(x,y)
        #self.x = x
        #self.y = y

        self.xdir = 2
        self.ydir = 2
        
        self.tile_w = tile_w
        self.tile_h = tile_h

    def update(self):
        self.x += self.xdir
        if self.x<0 or self.x>SCR_W :
            self.xdir = -self.xdir
        self.y += self.ydir
        if self.y<0 or self.y>SCR_H :
            self.ydir = -self.ydir

    def draw(self,screen,tiles):
        pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x-4,self.y-4,8,8))
