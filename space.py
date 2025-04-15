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
        self.player = None
        return temp
    
    def get_walls(self):
        walls = [1, 1, 1, 1]  # Start assuming walls in all directions
        y, x = self.pos
        for n in self.neighbors:
            if n.pos == (y-1, x):
                walls[0] = 0  # North is open
            if n.pos == (y, x+1):
                walls[1] = 0  # East is open
            if n.pos == (y+1, x):
                walls[2] = 0  # South is open
            if n.pos == (y, x-1):
                walls[3] = 0  # West is open
        return walls

    def remove_neighbor(self, neighbor):
        print(self.pos)
        for n in self.neighbors:
            print(n.pos)
        print("\n")
        self.neighbors.remove(neighbor)




