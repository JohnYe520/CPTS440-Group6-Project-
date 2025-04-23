from typing import List
import numpy as np
from player import Player
from space import Space
from wall import Wall
from astarpathfinding import a_star_path

#the board is a 9X9 grid of tuples ([int], int).
#   -The first element is the wall state array, the second number is the player number
#   WALL STATE ARRAY:
#       -The array is of size 4, with each element representng an adjacent wall, starting with the north wall at position 0 and going clockwise.
#           -[N,E,S,W]
#       -0 represents no wall
#       -1 represents that there is a wall.
#           - if a player is in a square they cannot move to another square if there is a wall in that direction.
#           - edge squares will always show the outside edge as having a wall.
#           - EX: the grid position (0,0) will have the wall state [1,0,0,1] at the start of the game.
#   PLAYER NUMBER:
#       - identifies a player.
#       - 0 is reserved for an empty square, any other integer may represent a player although it uses 1 and 2 for simplicity
# 
#   EXAMPLE BOARDSTATE WITH 3X3 GRID AT THE START OF A GAME
#   [([1,0,0,1],0), ([1,0,0,0],1), ([1,1,0,0],0)
#    ([0,0,0,1],0), ([0,0,0,0],0), ([0,1,0,0],0)
#    ([0,0,1,1],0), ([0,0,1,0],2), ([0,1,1,0],0)]
#    - no walls have been placed, the only walls are the outside edges.
#   
#   EXAMPLE BOARDSTATE AFTER A WALL HAS BEEN PLACED BETWEEN THE FOR SQUARES (0,0), (0,1), (1,0), (1,1)
#   [([1,0,1,1],0), ([1,0,1,0],1), ([1,1,0,0],0)
#    ([1,0,0,1],0), ([1,0,0,0],0), ([0,1,0,0],0)
#    ([0,0,1,1],0), ([0,0,1,0],2), ([0,1,1,0],0)]
#
#       You can think of the wall array as a list of possible move for a player on that square, 
#       so in the above example player 1 cannot move north or south as there is a wall in that direction

# the parameter input is used to initialize a boardstate with an already established one.
# if input is empty, a default boardstate of size 9 will be used.
# if you wish to change the board size, initialize the BoardState as BoardState(size=x) where x is the custom size
#   - x can be any positive odd integer. if x does not meet those criteria it will default to 9 (the size needs to be odd so that the players will start in the middle square on their respective sides)
# playerCount is the number of players on the board, this defaults to 2
class BoardState:
    def __init__(self, *args, size=9, playerCount=2):

        if len(args) == 1 and isinstance(args[0], BoardState): # branch for copying a previous board state
            input = args[0]
            self.size = input.size
            self.board = np.copy(input.board)
            self.players = input.players
            self.hWalls = input.hWalls
            self.vWalls = input.vWalls

        else:
            if size > 1 and size % 2 != 0:
                self.size = size
            else:
                self.size = 9
            self.board = np.empty((self.size, self.size), dtype=object) # an ndarray from numpy library
            for r in range(self.size):
                for c in range(self.size):
                    self.board[r,c] = Space(r,c) # fill the board with Space objects
            for r in range(self.size):
                for c in range(self.size):
                    self.add_neighbors(r,c) # assign spaces to their neighbors
            
            self.wall_init() # create all possible wall placements
            self.player_init(playerCount) # create and place players

    # moves a player to a desired spot on the board, used for handling logic of 1 player jumping over another, as well as testing purposes
    def teleport_player(self, player_num, y, x):
        player = self.players[player_num - 1]
        self.board[player.Y, player.X].remove_player()
        player.move(x, y)
        self.board[y, x].insert_player(player.PlayerNo)

    # initializes two arrays of Wall objects, one for horizontal walls, one for vertical walls; called in the constructor
    # since walls block two pairs of spaces, there are (board.size-1)^2 possible locations for horizontal walls and an equal number for vertical walls
    # since some possible wall placements overlap with others, we must also include those conflicting walls as neighbors for when the walls are activated, so we can set them as illegal moves
    def wall_init(self):
        self.hWalls = []
        self.vWalls = []
        for r in range(self.size-1):
                for c in range(self.size-1):
                    hWall = Wall([self.board[r,c],self.board[r+1,c],self.board[r,c+1],self.board[r+1,c+1]])
                    vWall = Wall([self.board[r,c],self.board[r,c+1],self.board[r+1,c],self.board[r+1,c+1]])
                    
                    # set conflicting wall placements as neighbors of each other; currently only considers conflicting walls in same direction
                    # Connect horizontally adjacent horizontal walls that might overlap
                    if c != 0:
                        hWall2 = self.hWalls[-1]
                        hWall.add_neighbor(hWall2)
                        hWall2.add_neighbor(hWall)
                        # Removed unnecessary vertical wall connections
                    
                    # Connect vertically adjacent vertical walls that might overlap
                    if r != 0:
                        v_index = (r-1) * (self.size-1) + c
                        vWall2 = self.vWalls[v_index]
                        vWall.add_neighbor(vWall2)
                        vWall2.add_neighbor(vWall)

                    # Consider wall of different orientation at the same position to be different
                    hWall.add_neighbor(vWall)
                    vWall.add_neighbor(hWall)
                        
                    self.hWalls.append(hWall)
                    self.vWalls.append(vWall)

    # initializes each Player object; called in the constructor. Defaults to 2 players if playerCount is more than 4 or less than 2
    # Each player starts in the middle of one side of the board. Player objects store their location, and spaces on the board store the player
    # players are initialized with (x,y,playerNo), but all other instances of coordinates are reversed (y,x) for printing purposes
    def player_init(self, playerCount):
        if playerCount > 4 or playerCount < 2:
                playerCount = 2
        self.players = []
        self.players.append(Player(self.size//2, 0, 1)) # player 1: starts at north edge of board
        self.players.append(Player(self.size//2, self.size-1, 2)) # player 2: starts at south edge of board
        if playerCount >= 3:
                self.players.append(Player(self.size // 2, 0, 3)) # player 3: starts at north edge of board? (should be east or west)
                if playerCount == 4:
                    self.players.append(Player(self.size // 2, self.size-1, 4)) # player 4: starts at south edge of board? (should be east or west)
        for p in self.players:
                self.board[p.Y, p.X].insert_player(p.PlayerNo)

    # designates the neighboring spaces for each space; called in the constructor
    # each space keeps track of the spaces that it can connect to. When a wall is activated, the respective neighbor is removed from that array
    def add_neighbors(self, i, j):
        space = self.board[i,j]
        if i > 0: # not on north edge
            space.insert_neighbor(self.board[i-1,j])
        if i < self.size-1: # not on south edge
            space.insert_neighbor(self.board[i+1,j])
        if j > 0: # not on west edge
            space.insert_neighbor(self.board[i,j-1])
        if j < self.size-1: # not on east edge
            space.insert_neighbor(self.board[i,j+1])
            
    # To place a wall use the coordinates of two directly-diagonal board spaces as the first two parameters for the place_wall function. 
    # These coordinates define the 2x2 grid of cells that the wall will be placed between.
    # Any two coordinates should work, as long as they are directly diagonal to each other. 
    # The final parameter of the place_wall function is the direction of the wall that will be placed, 0 is for a horizontal wall, 1 is for a vertical wall.
    # walls have four designated spaces, only 1 horiz and 1 vert can have the same set of spaces
    def place_wall(self, corner1, corner2, direction): # 0 for horizontal, 1 for vertical
        # 1. Try to place the wall tentatively
        wall = self.find_wall(self.board[corner1[0], corner1[1]], self.board[corner2[0], corner2[1]], direction)
        if wall is None or wall.set:
            return False  # Already set or invalid

        # Save current state for rollback
        removed_neighbors = []
        for i in range(0, 4, 2):
            s1, s2 = wall.spaces[i], wall.spaces[i+1]
            if s2 in s1.neighbors:
                s1.neighbors.remove(s2)
                removed_neighbors.append((s1, s2))
            if s1 in s2.neighbors:
                s2.neighbors.remove(s1)
                removed_neighbors.append((s2, s1))

        wall.set = True
        for n in wall.neighbors:
            n.set = True

        # 2. Check if both players have a path
        path1 = a_star_path(self, 1)
        path2 = a_star_path(self, 2)
        valid = path1 is not None and path2 is not None

        # 3. Rollback if not valid
        if not valid:
            # Undo wall
            wall.set = False
            for n in wall.neighbors:
                n.set = False
            for s1, s2 in removed_neighbors:
                s1.neighbors.append(s2)
            return False

        return True

    # helper function, returns the first wall in the list that contains the two desired spaces. 
    # Direction is boolean, determines if we check the horizontal wall list (0) or vertical wall list (1)
    # No return if wall is not found
    def find_wall(self, space1, space2,direction)->Wall:
        if direction == 0:
            for h in self.hWalls:
                if space1 in h.spaces and space2 in h.spaces:
                    return h

        elif direction == 1:
            for v in self.vWalls:
                if space1 in v.spaces and space2 in v.spaces:
                    return v

    # moves the player 1 space in the desired direction; does not check for walls
    # external game logic should check for valid moves and players before calling this function
    def move_player(self, player_num, direction):
            player = self.players[player_num-1]
            self.board[player.Y,player.X].remove_player()
            if direction == 0: # north
                player.move(player.X,player.Y-1)               
            elif direction == 1: # east
                player.move(player.X+1,player.Y)     
            elif direction == 2: # south
                player.move(player.X,player.Y+1) 
            elif direction == 3: # west
                player.move(player.X-1,player.Y)
            else:
                raise ValueError ("Invalid direction")
            self.board[player.Y,player.X].insert_player(player_num)

    # prints the board state, used when print(BoardState) is called
    def __str__(self):
        grid_str = ""
        for r in range(self.size):
            for c in range(self.size):
                space = self.board[r,c]
                if space.player is None: # space is empty
                        grid_str += "0"
                else:
                        grid_str += f"{space.player}" # print player num
                if c < self.size-1: # 1 less vertical wall per row than spaces
                    space2 = self.board[r,c+1]
                    wall = self.find_wall(space,space2,1)
                    if wall.set: # wall is active
                         grid_str += "\\"
                    else:
                         grid_str += "|"
            grid_str += "\n"
            if r < self.size-1: # 1 less row of horizontal walls than rows of spaces
                for c in range(self.size):
                    space = self.board[r,c]
                    space2 = self.board[r+1,c]
                    wall = self.find_wall(space,space2,0)
                    if wall.set: # wall is active
                        grid_str += "\\"
                    else:
                        grid_str += "-"
                    grid_str += " "
                grid_str += "\n"       
        return grid_str
    
### Testing code
# board = BoardState(size=5)

# board.place_wall((0,0), (1,1), 1)

# board.move_player(1, 2)
# board.move_player(2, 1)

# print(board)

# board2 = BoardState(board)
# print(board2)



