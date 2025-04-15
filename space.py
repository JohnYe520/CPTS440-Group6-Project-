from asyncio.windows_events import NULL
import player


class Space:
    def __init__(self,y,x):
        self.pos = (y,x)
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
    
    def get_walls(self):
        walls = [0,0,0,0]
        y,x = self.pos
        for n in self.neighbors:
            if n.pos == (y-1,x):
                walls[0] = 1
            if n.pos == (y,x+1):
                walls[1] = 1
            if n.pos == (y+1,x):
                walls[2] = 1
            if n.pos == (y,x-1):
                walls[3] = 1
        return walls

    def remove_neighbor(self, neighbor):
        print(self.pos)
        for n in self.neighbors:
            print(n.pos)
        print("\n")
        self.neighbors.remove(neighbor)




