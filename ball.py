import random
import pygame
import math

from globalconst import *
from gameobjects import *
from sound import *

BALL__SPEED_DIV=8*4                  # slows down all ball movement
BALL__SPEED_COLLISION_MULT_GROUND=80 # in % per impact
BALL__WALL_HEIGHT=12
BALL_SHADOW_COLOR=(0,96,0)

class Ball(GameObject):

    def __init__(self, gamestate):
        super(Ball, self).__init__(0, 0, 'o')

        #self.tile=tile # set by super()
        self.width=5    # to match sprite
        self.height=4   # to match sprite

        #self.x=0       # set by respawn()
        #self.y=0       # set by respawn()
        #self.z=0       # set by respawn(), ground at 0, positive up
        #self.xdir=0    # set by respawn(), velocity in pixels per frame
        #self.ydir=0    # set by respawn(), velocity in pixels per frame
        #self.zdir=0    # set by respawn(), velocity in pixels per frame
        self.respawn(gamestate)

    def stop(self):

        self.z=0
        self.xdir=0
        self.ydir=0
        self.zdir=0

    def respawn(self, gamestate):

        # default
        self.x=self.spawnx
        self.y=self.spawny
        self.z=8
        self.xdir=0
        self.ydir=0
        self.zdir=0

        # find and use random 'o' in level
        spawnPoints=[]
        for y in range(LEV_H):
            for x in range(LEV_W):
                if gamestate.getLevel()[y][x]=='o':
                    spawnPoints.append([x*8+2,y*8+2])
        spawnPoint=random.choice(spawnPoints)
        self.x=spawnPoint[0]
        self.y=spawnPoint[1]

    def __getLevelTile(self, gamestate): # at current x y

        tileX=round(self.x/TILE_W)
        if tileX<0:
            tileX=0
        if tileX>LEV_W-1:
            tileX=LEV_W-1

        tileY=round(self.y/TILE_H)
        if tileY<0:
            tileY=0
        if tileY>LEV_H-1:
            tileY=LEV_H-1

        return gamestate.getLevel()[tileY][tileX]

    def kick(self, xdir, ydir, zdir):

            self.xdir=xdir
            self.ydir=ydir
            self.zdir=zdir

            playSound('kick')

    def update(self, gamestate):

        # move z
        oldZ=self.z
        self.zdir-=1 # gravity
        self.z+=self.zdir/BALL__SPEED_DIV

        # collide z
        levelTile=self.__getLevelTile(gamestate)
        if levelTile=="#":
            if self.z<BALL__WALL_HEIGHT:
                # bounce off wall top
                self.zdir=math.fabs(self.zdir) # don't lose velocity so ball wont stop on walls
                self.z=oldZ
        elif levelTile==".":
            if self.z<BALL__WALL_HEIGHT:
                # goal
                gamestate.points+=1
                self.respawn(gamestate)
                playSound('whistle')
        else: # levelTile!="#"
            if self.z<0:
                # bounce off ground
                if self.zdir>-5: # snap to 0?
                    self.zdir=0
                    self.xdir=0
                    self.ydir=0
                self.zdir=math.fabs(self.zdir * BALL__SPEED_COLLISION_MULT_GROUND/100)
                self.xdir=          self.xdir * BALL__SPEED_COLLISION_MULT_GROUND/100
                self.ydir=          self.ydir * BALL__SPEED_COLLISION_MULT_GROUND/100
                self.z=oldZ

        # move x
        oldX=self.x
        oldLevelTile=self.__getLevelTile(gamestate)
        self.x+=self.xdir/BALL__SPEED_DIV
        levelTile=self.__getLevelTile(gamestate)

        # collide x
        hit=False
        if self.x<0:
            hit=True
        if self.x>SCR_W:
            hit=True
        if levelTile=="#" and self.z<BALL__WALL_HEIGHT:
            hit=True
        if hit:
            self.xdir=-self.xdir
            self.x=oldX

        # move y
        oldY=self.y
        oldLevelTile=self.__getLevelTile(gamestate)
        self.y+=self.ydir/BALL__SPEED_DIV
        levelTile=self.__getLevelTile(gamestate)

        # collide y
        hit=False
        if self.y<0:
            hit=True
        if self.y>SCR_H:
            hit=True
        if levelTile=="#" and self.z<BALL__WALL_HEIGHT:
            hit=True
        if hit:
            self.ydir=-self.ydir
            self.y=oldY

        # collide worms
        for worm in gamestate.getWorms():
            if worm.collide_head(self) and self.z<8:
                self.respawn(gamestate)


    def drawShadow(self, screen, tiles):

        ## shadow: simple
        #if self.z<BALL__WALL_HEIGHT:
        #    pygame.draw.rect(screen,BALL_SHADOW_COLOR,pygame.Rect(self.x,self.y,self.width,self.height))

        # shadow: size-changing
        if self.z<BALL__WALL_HEIGHT:
            shadowShrinkageX=self.z/8
            shadowShrinkageXMax=self.width/2-1
            if shadowShrinkageX>shadowShrinkageXMax:
                shadowShrinkageX=shadowShrinkageXMax
            shadowShrinkageY=self.z/8
            shadowShrinkageYMax=self.height/2-1
            if shadowShrinkageY>shadowShrinkageYMax:
                shadowShrinkageY=shadowShrinkageYMax
            pygame.draw.rect(screen,BALL_SHADOW_COLOR,pygame.Rect(self.x+shadowShrinkageX,self.y+1+shadowShrinkageY,self.width-2*shadowShrinkageX,self.height-2*shadowShrinkageY))

    def draw(self, screen, tiles, gamestate):

        ## above wall indicator
        ## replaced by shadow disappearing
        #if self.z>BALL__WALL_HEIGHT:
        #    x=round(self.x+self.width/2)-1
        #    y=self.y+self.height/2
        #    pygame.draw.line(screen,(255,64,32),(x-2,y-BALL__WALL_HEIGHT),(x+2,y-BALL__WALL_HEIGHT))
        #    pygame.draw.line(screen,(255,64,32),(x,y),(x,y-BALL__WALL_HEIGHT))

        # ball sprite
        # offset to match bounding box
        screen.blit(tiles[self.tile],(self.x-1,self.y-3-self.z))
