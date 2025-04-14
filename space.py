from asyncio.windows_events import NULL
import player


class Space:
    #def __init__(self, walls = [0,0,0,0]):
     #   self.walls = walls
      #  self.player = NULL
    def __init__(self):
        self.neighbors = []
        self.player = NULL

    def insert_neighbor(self, space):
        self.neighbors.append(space)
        
    def insert_player(self, playerNo):
        self.player = playerNo

    def remove_player(self):
        temp = self.player
        self.player = NULL
        return temp

    #def placeWall(self, walls):
     #   self.walls = walls

    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)




