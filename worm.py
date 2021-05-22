import gameobjects
from time import time


class Worm(gameobjects.GameObject):
    def __init__(self,x,y,tile_w,tile_h):
        super(Worm, self).__init__(x,y)
        #self.x = x
        #self.y = y

        self.tile_w = tile_w
        self.tile_h = tile_h

        self.head =[x,y]
        self.body=[]

        self.tiles=["H","B"]

        self.last_move_time= 0
        self.move_time     = 0.2

        pass


    def getSprite(self,sprite,tiles):
        return tiles[sprite]

    def update(self):
        if self.last_move_time +self.move_time< time() :
            #update the position
            self.head[0] += self.xdir
            self.head[1] += self.ydir

            self.last_move_time = time()
        pass

    def draw(self,screen,tiles):
        self.getSprite("H",tiles)
        #draw the head

        screen.blit(tiles[self.tiles[0]], (self.head[0] * self.tile_w, self.head[1] * self.tile_h))
        #draw the body
        for part in self.body:
            continue

        pass