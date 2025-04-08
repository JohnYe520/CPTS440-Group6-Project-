from asyncio.windows_events import NULL
import player


class Space:
    #def __init__(self, walls = [0,0,0,0]):
     #   self.walls = walls
      #  self.player = NULL
    def __init__(self, neighbors):
        self.neighbors = neighbors
        self.player = NULL

    def insertPlayer(self, playerNo):
        self.player = playerNo

    def removePlayer(self):
        temp = self.player
        self.player = NULL
        return temp

    #def placeWall(self, walls):
     #   self.walls = walls

    def removeNeighbor(self, neighbor):
        self.neighbors.remove(neighbor)




