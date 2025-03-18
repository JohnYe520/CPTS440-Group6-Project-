import numpy as np
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
#       - 0 is reserved for an empty square, any other integer may represent a player although it would be best to stick to 1 and 2 for simplicity
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


class BoardState:
    def __init__(self, input=None, start=False):
        self.size = 9
        if start == True:
            self.board = np.empty((self.size, self.size), dtype=object)
            for r in range(self.size):
                for c in range(self.size):
                    self.board[r,c] = self.create_cell(r,c, self.size)
        else:
            self.board = input

    def create_cell(self, r, c, size):
        walls = [0,0,0,0]

        if r == 0:  # Top row
            walls[0] = 1
        if r == size - 1: # Bottom Row
            walls[2] = 1
        if c == 0: # left collumn
            walls[3] = 1
        if c == size - 1: # right collumn
            walls[1] = 1
        
        return (np.array(walls), 0)
    
board = BoardState(start=True)

print(board.board)