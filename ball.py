import pygame
from globalconst import *
from gameobjects import *

class Ball(GameObject):

    def __init__(self, x, y, tile):
        self.SPEED_DIV = 8*2
        self.SPEED_COLLISION_MULT_GROUND = 80 # in %
        self.WALL_HEIGHT = 12
        super(Ball, self).__init__(x, y, tile)
        #self.tile = tile
        self.width = 5
        self.height = 4
        #self.x = x
        #self.y = y
        self.z = 0
        self.size = 8
        self.xdir = 20
        self.ydir = 20
        self.zdir = 31

    def getLevelTile(self, gamestate, x, y): # private
        tileX=round(x/TILE_W)
        if tileX<0:
            tileX=0
        if tileX>LEV_W-1:
            tileX=LEV_W-1
        tileY=round(y/TILE_H)
        if tileY<0:
            tileY=0
        if tileY>LEV_H-1:
            tileY=LEV_H-1
        return gamestate.getLevel()[tileY][tileX]

    def update(self, gamestate):

        # move z
        oldLevelTile=self.getLevelTile(gamestate,self.x,self.y)
        if self.z > 0:
            self.zdir -= 1
        self.z += self.zdir / self.SPEED_DIV

        # collide z
        if oldLevelTile==" ": # above grass
            if self.z < 0:
                self.z = 0
                self.zdir = -self.zdir * self.SPEED_COLLISION_MULT_GROUND/100
                self.xdir =  self.xdir * self.SPEED_COLLISION_MULT_GROUND/100
                self.ydir =  self.ydir * self.SPEED_COLLISION_MULT_GROUND/100
        else: # above wall
            if self.z < self.WALL_HEIGHT:
                self.z = self.WALL_HEIGHT
                self.zdir = -self.zdir
                self.xdir =  self.xdir
                self.ydir =  self.ydir

        # move x
        oldLevelTile=self.getLevelTile(gamestate,self.x,self.y)
        oldX = self.x
        self.x += self.xdir / self.SPEED_DIV
        levelTile=self.getLevelTile(gamestate,self.x,self.y)

        # collide x
        hit = False
        if self.x < 0:
            hit = True
        if self.x > SCR_W - self.size:
            hit = True
        if levelTile!=" " and self.z<self.WALL_HEIGHT:
            hit = True
        if hit:
            self.xdir = -self.xdir
            self.x = oldX

        # move y
        oldLevelTile=self.getLevelTile(gamestate,self.x,self.y)
        oldY = self.y
        self.y += self.ydir / self.SPEED_DIV
        levelTile=self.getLevelTile(gamestate,self.x,self.y)

        # collide y
        hit = False
        if self.y < 0:
            hit = True
        if self.y > SCR_H - self.size:
            hit = True
        if levelTile!=" " and self.z<self.WALL_HEIGHT:
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

        ## height hint
        #if self.z>self.WALL_HEIGHT:
        #    pygame.draw.line(screen,(64,64,64),(self.x+self.width/2,self.y+self.height/2),(self.x+self.width/2,self.y+self.height/2-self.z))

        # ball sprite
        screen.blit(tiles[self.tile],(self.x-1,self.y-3-self.z))
