import pygame

from globalconst import *
from gameobjects import *
from sound import *

BALL__SPEED_DIV=8*4                  # slows down all ball movement
BALL__SPEED_COLLISION_MULT_GROUND=80 # in % per impact
BALL__WALL_HEIGHT=12
BALL_SHADOW_COLOR=(0,96,0)

class Ball(GameObject):

    def __init__(self, x, y, tile):
        super(Ball, self).__init__(x, y, tile)

        #self.tile=tile # set by super()
        self.width=5    # to match sprite
        self.height=4   # to match sprite

        #self.x=x       # set by super()
        #self.y=y       # set by super()
        self.z=40       # ground at 0, positive up

        self.xdir=0     # velocity in pixels per frame
        self.ydir=0     # velocity in pixels per frame
        self.zdir=0     # velocity in pixels per frame

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

    def kick(self, xdir, ydir):

        if self.z<8:
            self.xdir=xdir*5
            self.ydir=ydir*5
            self.zdir=20
            playSound('kick')

    def update(self, gamestate):

        # move z
        oldLevelTile=self.__getLevelTile(gamestate)
        if self.z>0:
            self.zdir-=1
        self.z+=self.zdir/BALL__SPEED_DIV

        # collide z
        if oldLevelTile==" ": # above grass
            if self.z<0:
                self.z=0
                if self.zdir>-5:
                    self.zdir=0
                    self.xdir=0
                    self.ydir=0
                self.zdir=-self.zdir * BALL__SPEED_COLLISION_MULT_GROUND/100
                self.xdir= self.xdir * BALL__SPEED_COLLISION_MULT_GROUND/100
                self.ydir= self.ydir * BALL__SPEED_COLLISION_MULT_GROUND/100
        else: # above wall
            if self.z<BALL__WALL_HEIGHT:
                self.z=BALL__WALL_HEIGHT
                self.zdir=-self.zdir
                self.xdir= self.xdir
                self.ydir= self.ydir

        # move x
        oldLevelTile=self.__getLevelTile(gamestate)
        oldX=self.x
        self.x+=self.xdir/BALL__SPEED_DIV
        levelTile=self.__getLevelTile(gamestate)

        # collide x
        hit=False
        if self.x<0:
            hit=True
        if self.x>SCR_W:
            hit=True
        if levelTile!=" " and self.z<BALL__WALL_HEIGHT:
            hit=True
        if hit:
            self.xdir=-self.xdir
            self.x=oldX

        # move y
        oldLevelTile=self.__getLevelTile(gamestate)
        oldY=self.y
        self.y+=self.ydir/BALL__SPEED_DIV
        levelTile=self.__getLevelTile(gamestate)

        # collide y
        hit=False
        if self.y<0:
            hit=True
        if self.y>SCR_H:
            hit=True
        if levelTile!=" " and self.z<BALL__WALL_HEIGHT:
            hit=True
        if hit:
            self.ydir=-self.ydir
            self.y=oldY

    def draw(self, screen, tiles):

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
