from direct.showbase.ShowBase import ShowBase

from mapmanager import Mapmanager
from hero import Hero
from control_keys import *

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x, y = self.land.loadLand("land.txt")
        self.hero = Hero((x//2, y//2, 2), self.land)
        self.btype = 1
        base.camLens.setFov(90)

        base.accept(key_plane, self.land.planeLand)
        base.accept(key_loadland, self.land.loadLand, ["land.txt"])
        base.accept(key_savemap, self.land.saveMap, ["my_map.dat"])
        base.accept(key_loadmap, self.land.loadMap, ["my_map.dat"])

game = Game()
game.run()