import pygame
from globalconst import *
from gameobjects import *

class Bird(GameObject):

    def __init__(self, x, y, tile):
        self.SPEED_DIV = 8*2
        self.WALL_HEIGHT = 12
        super().__init__(x, y, tile)
        #self.tile = tile
        self.width = 6
        self.height = 2
        #self.x = x
        #self.y = y
        self.z = 0
        self.size = 8
        self.xdir = 10
        self.ydir = 10
        self.zdir = 15


    def update(self, gamestate):

        # move x
        oldX = self.x
        self.x += self.xdir / self.SPEED_DIV
        # collide x
        hit = False
        if self.x < 0:
            hit = True
        if self.x > SCR_W - self.size:
            hit = True

        if hit:
            self.xdir = -self.ydir
            self.x = oldX

        # move y
        oldY = self.y
        self.y += self.ydir / self.SPEED_DIV

        # collide y
        hit = False
        if self.y < 0:
            hit = True
        if self.y > SCR_H - self.size:
            hit = True

        if hit:
            self.ydir = -self.ydir
            self.y = oldY

        # int attributes
        #self.x = round( self.x )
        #self.y = round( self.y )
        #self.z = round( self.z )
        #self.xdir = round( self.xdir )
        #self.ydir = round( self.ydir )
        #self.zdir = round( self.zdir )

    def get_eaten(self):
        pass

    def drawShadow(self,screen,tiles):

        shadowColor = (0,96,0)

        # shadow: simple
        pygame.draw.rect(screen,shadowColor,pygame.Rect(self.x+1,self.y+12,self.width,self.height))


    def draw(self,screen,tiles,gamestate):

        # bounding box at z=0
        if DEBUG_MODE:
            pygame.draw.rect(screen,(255,0,0),pygame.Rect(self.x,self.y,self.width,self.height))

        # ball sprite
        screen.blit(tiles[self.tile],(self.x,self.y-self.z))
