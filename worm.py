import gameobjects
from time import time
from globalconst import *

class rect():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height = height

class Worm(gameobjects.GameObject):
    def __init__(self,x,y):
        super(Worm, self).__init__(x,y)
        #self.x = x
        #self.y = y


        self.head =[x,y]
        self.body=[]

        self.tiles=["H","B"]

        #worm move timer
        self.last_move_time= 0
        self.move_time     = 0.2

        #worm body addition timer
        self.steps_till_addition = 4
        self.step_counter = 0

        self.move_dir=[0,0]

        self.debugList =[]


        self._MOVEMENTS = [
            [-1,0],
            [1,0],
            [0,-1],
            [0,1],
        ]

        self._dir_ops=[2,1,4,3]


    def getSprite(self,sprite,tiles):
        return tiles[sprite]


    def update(self):
        self.debugList =[]

        #when we should move
        if self.last_move_time +self.move_time< time() :

            self.xdir = self._MOVEMENTS[self.facedir][0]
            self.ydir = self._MOVEMENTS[self.facedir][1]

            #if we should move

            #did a dir change occure
            if True:

                #check future collision with self
                if self._collides_body(rect((self.x +self.xdir)* self.width, (self.y+self.ydir )* self.height, self.width, self.height)) == True:
                    #print("Collided with self!!")
                    return False
                    # here reset the worm parts

                #if a map was given check collision with it
                if level != None:
                    if level[self.y+self.ydir][self.x+self.xdir] != " " :
                        #print("Collided with a wall D:")
                        return False



                #update all the bodys first
                if len(self.body)>0:
                    for part_idx in range(len(self.body),0,-1):
                        #part_tmp = self.body[part_idx-1]
                        if part_idx-1 ==0:
                            self.body[part_idx-1]=[*self.head]
                        else:
                            self.body[part_idx-1]=[*self.body[part_idx-2]]


                #add a body part
                if self.step_counter >= self.steps_till_addition:
                    self.step_counter = 0
                    self.body.insert(0,[*self.head])


                self.last_move_time = time()
                self.step_counter+=1

                #update the position
                self.head[0] += self.xdir
                self.head[1] += self.ydir

                self.x += self.xdir
                self.y += self.ydir




    def _gen_collide(self,obj_a,obj_b):
        if obj_a[0] < obj_b.x + obj_b.width and \
            obj_a[0] + self.width > obj_b.x and \
            obj_a[1] < obj_b.y + obj_b.height and \
            obj_a[1] + self.height > obj_b.y:

            self.debugList.append([obj_a[0], obj_a[1],self.width,self.height])
            self.debugList.append([obj_b.x, obj_b.y,obj_b.width,obj_b.height])

            return True
        return False

    def _collides_body(self,game_object):
        collides = False

        for part in self.body:
            part_coords=[part[0]*self.width,part[1]*self.height]
            if self._gen_collide(part_coords,game_object) == True:
                return True
        return collides

    def collide_head(self,game_object):
        if self.head[0]*self.width < game_object.x + game_object.width and \
            self.head[0]*self.width + self.width > game_object.x and \
            self.head[1]*self.height < game_object.y + game_object.height and \
            self.head[1]*self.height + self.height > game_object.y:
            #debugList.append([self.x, self.y])
            #debugList.append([game_object.x, game_object.y])

            return True
        else:
            return False

    def collides(self, game_object):
        if self.head[0]*self.width < game_object.x + game_object.width and \
            self.head[0]*self.width + self.width > game_object.x and \
            self.head[1]*self.height < game_object.y + game_object.height and \
            self.head[1]*self.height + self.height > game_object.y:
            #debugList.append([self.x, self.y])
            #debugList.append([game_object.x, game_object.y])

            return True
        else:
            col=self._collides_body(game_object)
            return col
        return False


    def draw(self,screen,tiles):
        #self.getSprite("H",tiles)
        #draw the head

        screen.blit(tiles[self.tiles[0]], (self.head[0] * self.width, self.head[1] * self.height))

        #draw the body
        for part in self.body:
            screen.blit(tiles["B"], (part[0] * self.width, part[1] * self.height))



    def moveLeft(self):

        if self.facedir != RIGHT:
            self.facedir =LEFT

    def moveRight(self):
        if self.facedir!=LEFT:
            self.facedir =RIGHT

    def moveUp(self):
        if self.facedir!=DOWN:
            self.facedir = UP

    def moveDown(self):
        if self.facedir!=UP:
            self.facedir = DOWN