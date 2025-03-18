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
    def place_wall(self, corner1, corner2, direction): # 0 for horizontal, 1 for verticle
            if abs(corner1[0] - corner2[0]) != 1 or abs(corner1[1] - corner2[1]) != 1: # check that the rows are 1 apart # checks if the collumns are 1 aprt.
                return False
            elif direction == 0:
                if (corner2[0] > corner1[0]): # corner1 is above corner2
                    self.__place_wall_horizontal(corner1, corner2)
                    if (corner2[1] > corner1[1]): # corner 1 is to the left
                        self.__place_wall_horizontal((corner1 := [*corner1[:1], corner1[1] + 1]), (corner2 := [*corner2[:1], corner2[1] - 1]))
                    else:
                        self.__place_wall_horizontal((corner1 := [*corner1[:1], corner1[1] - 1]), (corner2 := [*corner2[:1], corner2[1] + 1]))
                else: #corner2 is above corner1
                    self.__place_wall_horizontal(self, corner2, corner1)
                    if (corner1[1] > corner2[1]): # corner 2 is to the left
                        self.__place_wall_horizontal((corner2 := [*corner2[:1], corner2[1] + 1]), (corner1 := [*corner1[:1], corner1[1] - 1]))
                    else:
                        self.__place_wall_horizontal((corner2 := [*corner2[:1], corner2[1] - 1]), (corner1 := [*corner1[:1], corner1[1] + 1]))
            
            elif direction == 1:
                if(corner2[1] > corner1[1]): #corner 1 is to the left of corner 2
                    self.__place_wall_verticle(corner1,corner2)
                    if (corner2[0] > corner1[0]): # corner1 is above corner2
                        self.__place_wall_verticle((corner1 := [corner1[0] + 1, *corner1[1:]]), (corner2 := [corner2[0] - 1, *corner2[1:]]))
                    else:
                        self.__place_wall_verticle((corner1 := [corner1[0] - 1, *corner1[1:]]), (corner2 := [corner2[0] + 1, *corner2[1:]]))
                else: #corner 2 is to the left of corner 1
                    self.__place_wall_verticle(corner2,corner1)
                    if (corner2[0] > corner1[0]): # corner2 is above corner1
                        self.__place_wall_verticle((corner2 := [corner2[0] + 1, *corner2[1:]]), (corner1 := [corner1[0] - 1, *corner1[1:]]))
                    else:
                        self.__place_wall_verticle((corner2 := [corner2[0] - 1, *corner2[1:]]), (corner1 := [corner1[0] + 1, *corner1[1:]]))

    
    
    def __place_wall_horizontal(self, above, below):
        above_walls, above_val = self.board[above[0], above[1]]
        below_walls, below_val = self.board[below[0], below[1]]

        above_walls[2] = 1  # South wall on the above cell
        below_walls[0] = 1  # North wall on the below cell

        self.board[above[0], above[1]] = (above_walls, above_val)
        self.board[below[0], below[1]] = (below_walls, below_val)

    def __place_wall_verticle(self, left, right):
        left_walls, left_val = self.board[left[0], left[1]]
        right_walls, right_val = self.board[right[0], right[1]]

        left_walls[1] = 1  # East wall on the left cell
        right_walls[3] = 1  # West wall on the right cell

        self.board[left[0], left[1]] = (left_walls, left_val)
        self.board[right[0], right[1]] = (right_walls, right_val)
    
    def __str__(self):
        grid_str = ""
        for r in range(self.size):
            row_str = ", ".join(
                f"[{walls.tolist()}, {val}]" for walls, val in self.board[r]
            )
            grid_str += f"{row_str}\n"
        return grid_str

### Testing code
board = BoardState(start=True)
print(board.board[0,0]) 
print(board.board[0,1])
print(board.board[1,0])
print(board.board[1,1])

board.place_wall((0,0), (1,1), 1)

print(board.board[0,0]) 
print(board.board[0,1])
print(board.board[1,0])
print(board.board[1,1])

print(board)
