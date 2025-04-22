import player

# a space on the board, which keeps track of neighboring spaces that can be reached from it (i.e. not blocked by a wall)
class Space:
    def __init__(self,y,x):
        self.pos = (y,x) # the space's designated position on the board
        self.neighbors = [] # the spaces that can be reached from this space; initially empty, since we have not necessarily created all its neighbors yet
        self.player = None # the number of the player on this space; does not contain the player object

    # adds a new space to the list of neighbors
    def insert_neighbor(self, space):
        self.neighbors.append(space)
    
    # sets this space as the location of the given player number
    def insert_player(self, playerNo):
        self.player = playerNo

    # removes and returns the player number
    def remove_player(self):
        temp = self.player
        self.player = None
        return temp
    
    # get the directions that are blocked from this space; checks each neighbor to see which direction they're in, and marks that direction in the list [N,E,S,W] as unblocked
    def get_walls(self):
        walls = [1, 1, 1, 1]  # Start assuming walls in all directions
        y, x = self.pos
        for n in self.neighbors:
            if n.pos == (y-1, x):
            #if n.pos == (y+1, x):
                walls[0] = 0  # North is open
            if n.pos == (y, x+1):
                walls[1] = 0  # East is open
                
            if n.pos == (y+1, x): #dont think is problem
                #print("if statement!")
            #if n.pos == (y-1, x):
                walls[2] = 0  # South is open
                
            if n.pos == (y, x-1):
                walls[3] = 0  # West is open
        #print("walls function: ", walls)
        return walls

    # removes the desired neighboring space from the list of neighbors
    def remove_neighbor(self, neighbor):
        # print(self.pos)
        # for n in self.neighbors:
        #     print(n.pos)
        # print("\n")
        self.neighbors.remove(neighbor)




