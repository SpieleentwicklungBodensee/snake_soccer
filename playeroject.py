from globalconst import *
from gameobjects import *

class Player(GameObject):
    def __init__(self, x, y, tile = None):
        GameObject.__init__(self, x, y, tile)
