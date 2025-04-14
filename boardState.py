from asyncio.windows_events import NULL
from typing import List
import numpy as np
from player import Player
from space import Space
from wall import Wall

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
class BoardState:
    def __init__(self, *args, size=9, playerCount=2):
        #self.size = 5
        if len(args) == 1 and isinstance(args[0], BoardState):
            input = args[0]
            self.size = input.size
            self.board = np.copy(input.board)
            self.players = input.players
            self.hWalls = input.hWalls
            self.vWalls = input.vWalls
            #self.player1 = input.player1
            #self.player2 = input.player2

        else:
            if size > 1 and size % 2 != 0:
                self.size = size
            else:
                self.size = 9
            self.board = np.empty((self.size, self.size), dtype=object)
            for r in range(self.size):
                for c in range(self.size):
                    #self.board[r,c] = self.__create_cell(r,c, self.size)
                    self.board[r,c] = Space(r,c)
            for r in range(self.size):
                for c in range(self.size):
                    self.add_neighbors(r,c)
            
            self.wall_init()
            self.player_init(playerCount)
            #player1_walls, player1_val = self.board[0, self.size // 2]
            #player2_walls, player2_val = self.board[self.size - 1, self.size // 2]
            #player1_val = 1
            #player2_val = 2
            #self.board[0, self.size // 2] = (player1_walls, player1_val)
            #self.board[self.size - 1, self.size // 2] = (player2_walls, player2_val)

            #self.player1 = ([0, self.size // 2], self.board[0, self.size // 2])
            #self.player2 = ([self.size - 1, self.size // 2], self.board[self.size - 1, self.size // 2])
        
    def wall_init(self):
        self.hWalls = []
        self.vWalls = []
        for r in range(self.size-1):
                for c in range(self.size-1):
                    hWall = Wall([self.board[r,c],self.board[r+1,c],self.board[r,c+1],self.board[r+1,c+1]])
                    vWall = Wall([self.board[r,c],self.board[r,c+1],self.board[r+1,c],self.board[r+1,c+1]])
                    if c != 0:
                        hWall2 = self.hWalls[-1]
                        hWall.add_neighbor(hWall2)
                        hWall2.add_neighbor(hWall)
                        vWall2 = self.vWalls[-1]
                        vWall.add_neighbor(vWall2)
                        vWall2.add_neighbor(vWall)
                    self.hWalls.append(hWall)
                    self.vWalls.append(vWall)
        # print(f"{len(self.hWalls)} horiz walls and {len(self.vWalls)} vert walls")
        # for w in range(len(self.hWalls)):
        #      print(len(self.hWalls[w].neighbors))
        #      print(len(self.vWalls[w].neighbors))

    def player_init(self, playerCount):
        if playerCount > 4 or playerCount < 2:
                playerCount = 2
        self.players = []
        self.players.append(Player(self.size//2, 0, 1))
        self.players.append(Player(self.size//2, self.size-1, 2))
        if playerCount >= 3:
                self.players.append(Player(self.size // 2, 0, 3))
                if playerCount == 4:
                    self.players.append(Player(self.size // 2, self.size-1, 4))
        for p in self.players:
                self.board[p.Y, p.X].insert_player(p.PlayerNo)

    def add_neighbors(self, i, j):
        # index = self.board.index(space)
        space = self.board[i,j]
        # print(i)
        # print(j)
        if i > 0:
            space.insert_neighbor(self.board[i-1,j])
        if i < self.size-1:
            space.insert_neighbor(self.board[i+1,j])
        if j > 0:
            space.insert_neighbor(self.board[i,j-1])
        if j < self.size-1:
            space.insert_neighbor(self.board[i,j+1])
            
    # To place a wall use the coordinates of two directly-diagonal board spaces as the first two parameters for the place_wall function. 
    #   These coordinates define the 2x2 grid of cells that the wall will be placed between.
    #   Any two coordinates should work, as long as they are directly diagonal to each other. 
    # The final parameter of the place_wall function is the direction of the wall that will be placed, 0 is for a horizontal wall, 1 is for a vertical wall.

    # walls have four designated spaces, only 1 horiz and 1 vert can have the same set of spaces
    def place_wall(self, corner1, corner2, direction): # 0 for horizontal, 1 for verticle
             if abs(corner1[0] - corner2[0]) != 1 or abs(corner1[1] - corner2[1]) != 1: # check that the rows are 1 apart # checks if the collumns are 1 aprt.
                 return False
             space1 = self.board[corner1[0],corner1[1]]
             # space2 = self.board[corner1[0],corner2[1]]
             # space3 = self.board[corner2[0],corner1[1]]
             space2 = self.board[corner2[0],corner2[1]]
             wall = self.find_wall(space1,space2,direction)
             return wall.wall_off()

                 # if (corner2[0] > corner1[0]): # corner1 is above corner2
                 #     self.__place_wall_horizontal(corner1, corner2)
                 #     if (corner2[1] > corner1[1]): # corner 1 is to the left
                 #         self.__place_wall_horizontal((corner1 := [*corner1[:1], corner1[1] + 1]), (corner2 := [*corner2[:1], corner2[1] - 1]))
                 #     else:
                 #         self.__place_wall_horizontal((corner1 := [*corner1[:1], corner1[1] - 1]), (corner2 := [*corner2[:1], corner2[1] + 1]))
                 # else: #corner2 is above corner1
                 #     self.__place_wall_horizontal(self, corner2, corner1)
                 #     if (corner1[1] > corner2[1]): # corner 2 is to the left
                 #         self.__place_wall_horizontal((corner2 := [*corner2[:1], corner2[1] + 1]), (corner1 := [*corner1[:1], corner1[1] - 1]))
                 #     else:
                 #         self.__place_wall_horizontal((corner2 := [*corner2[:1], corner2[1] - 1]), (corner1 := [*corner1[:1], corner1[1] + 1]))
            
             # elif direction == 1:
             #     if(corner2[1] > corner1[1]): #corner 1 is to the left of corner 2
             #         self.__place_wall_verticle(corner1,corner2)
             #         if (corner2[0] > corner1[0]): # corner1 is above corner2
             #             self.__place_wall_verticle((corner1 := [corner1[0] + 1, *corner1[1:]]), (corner2 := [corner2[0] - 1, *corner2[1:]]))
             #         else:
             #             self.__place_wall_verticle((corner1 := [corner1[0] - 1, *corner1[1:]]), (corner2 := [corner2[0] + 1, *corner2[1:]]))
             #     else: #corner 2 is to the left of corner 1
             #         self.__place_wall_verticle(corner2,corner1)
             #         if (corner2[0] > corner1[0]): # corner2 is above corner1
             #             self.__place_wall_verticle((corner2 := [corner2[0] + 1, *corner2[1:]]), (corner1 := [corner1[0] - 1, *corner1[1:]]))
             #         else:
             #             self.__place_wall_verticle((corner2 := [corner2[0] - 1, *corner2[1:]]), (corner1 := [corner1[0] + 1, *corner1[1:]]))
    def find_wall(self, space1, space2,direction)->Wall:
        if direction == 0:
            for h in self.hWalls:
                if space1 in h.spaces and space2 in h.spaces:
                    return h

        elif direction == 1:
            for v in self.vWalls:
                if space1 in v.spaces and space2 in v.spaces:
                    return v

    # external game logic should check for valid moves and players before calling this function
    def move_player(self, player_num, direction):
            
            # if player_num == 1:
            #     player = self.players[0]
            # elif player_num == 2:
            #     player = self.players[1]
            # else:
            #     raise ValueError("Invalid player number")
            player = self.players[player_num-1]
            #x = player[0]
            
            self.board[player.Y,player.X].remove_player()
            # print(player.Y,player.X,direction)
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
            # print(player.Y,player.X,direction)
            self.board[player.Y,player.X].insert_player(player_num)

            # if player_num == 1:
            #     self.players[0] = (player_location, self.board[player_location[0], player_location[1]])
            # elif player_num == 2:
            #     self.players[1] = (player_location, self.board[player_location[0], player_location[1]])

    def __set_player(self, location, new_player_num):
        # cell_walls = self.board[location[0], location[1]][0]
        # self.board[location[0], location[1]] = (cell_walls, new_player_num)
        player = self.players[new_player_num-1]
        self.board[player.Y,player.X].remove_player()
        y,x = location
        player.move(x,y)
        self.board[player.Y,player.X].insert_player(player.PlayerNo)
        

    # def __place_wall_horizontal(self, above, below):
    #     above_walls, above_val = self.board[above[0], above[1]]
    #     below_walls, below_val = self.board[below[0], below[1]]

    #     above_walls[2] = 1  # South wall on the above cell
    #     below_walls[0] = 1  # North wall on the below cell

    #     self.board[above[0], above[1]] = (above_walls, above_val)
    #     self.board[below[0], below[1]] = (below_walls, below_val)

    # def __place_wall_verticle(self, left, right):
    #     left_walls, left_val = self.board[left[0], left[1]]
    #     right_walls, right_val = self.board[right[0], right[1]]

    #     left_walls[1] = 1  # East wall on the left cell
    #     right_walls[3] = 1  # West wall on the right cell

    #     self.board[left[0], left[1]] = (left_walls, left_val)
    #     self.board[right[0], right[1]] = (right_walls, right_val)
    
    # def __create_cell(self, r, c, size):
    #     walls = [0,0,0,0]

    #     if r == 0:  # Top row
    #         walls[0] = 1
    #     if r == size - 1: # Bottom Row
    #         walls[2] = 1
    #     if c == 0: # left collumn
    #         walls[3] = 1
    #     if c == size - 1: # right collumn
    #         walls[1] = 1
        
    #     #return (np.array(walls), 0)
    #     return Space(walls)

    # def __str__(self):
    #     grid_str = ""
    #     for r in range(self.size):
    #         row_str = ", ".join(
    #             f"[{walls.tolist()}, {val}]" for walls, val in self.board[r]
    #         )
    #         grid_str += f"{row_str}\n"
    #     return grid_str

    # def get_walls(self,y,x):
    #     state = self.board(y,x)
    #     if y > 0 and self.board(y,x)

    def __str__(self):
        grid_str = ""
        for r in range(self.size):
            for c in range(self.size):
                space = self.board[r,c]
                if space.player is NULL:
                        grid_str += "0"
                else:
                        grid_str += f"{space.player}"
                if c < self.size-1:
                    space2 = self.board[r,c+1]
                    wall = self.find_wall(space,space2,1)
                    if wall.set:
                         grid_str += "\\"
                    else:
                         grid_str += "|"
            grid_str += "\n"
            if r < self.size-1:
                for c in range(self.size):
                    space = self.board[r,c]
                    space2 = self.board[r+1,c]
                    wall = self.find_wall(space,space2,0)
                    if wall.set:
                        grid_str += "\\"
                    else:
                        grid_str += "-"
                    grid_str += " "
                grid_str += "\n"

                        
        return grid_str
### Testing code
board = BoardState(size=5)

# board.place_wall((0,0), (1,1), 1)

# board.move_player(1, 2)
# board.move_player(2, 1)

# print(board)

# board2 = BoardState(board)
# print(board2)



