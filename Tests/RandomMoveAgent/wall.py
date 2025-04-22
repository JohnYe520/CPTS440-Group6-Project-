from asyncio.windows_events import NULL

# a possible wall to be placed on the board in order to block off access to spaces
# each wall "blocks" two pairs of spaces when activated by removing those spaces from each other's list of neighbors
# walls that overlap with each other cannot both be placed; when a wall is placed, its neighbors are marked as 'set' as well, and cannot be activated
class Wall:
    def __init__(self, spaces):
        self.spaces = spaces # the list of spaces that this wall will block when active
        self.set = False # whether or not this wall is active
        self.neighbors = [] # the list of walls that block some of the same spaces as this wall; current board logic only considers walls in same direction (horizontal or vertical) as each other

    # adds neighboring wall to list of neighbors
    def add_neighbor(self, wall):
        self.neighbors.append(wall)

    # if wall is not already active, tells designated spaces to remove each other from their list of neighbors, then marks the wall and its neighbors as set
    # always returns true, supposed to return false if wall is already set
    def wall_off(self):
        if not self.set:
            self.spaces[0].remove_neighbor(self.spaces[1])
            self.spaces[1].remove_neighbor(self.spaces[0])
            self.spaces[2].remove_neighbor(self.spaces[3])
            self.spaces[3].remove_neighbor(self.spaces[2])
            self.set = True
            for n in self.neighbors:
                n.set = True
        return self.set




