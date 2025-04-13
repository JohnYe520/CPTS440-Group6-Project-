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
    def __init__(self, *args, size=9):
        #self.size = 5
        if len(args) == 1 and isinstance(args[0], BoardState):
            input = args[0]
            self.size = input.size
            self.board = np.copy(input.board)
            self.player1 = input.player1
            self.player2 = input.player2

        else:
            if size > 1 and size % 2 != 0:
                self.size = size
            else:
                self.size = 9
            self.board = np.empty((self.size, self.size), dtype=object)
            for r in range(self.size):
                for c in range(self.size):
                    self.board[r,c] = self.__create_cell(r,c, self.size)
            
            player1_walls, player1_val = self.board[0, self.size // 2]
            player2_walls, player2_val = self.board[self.size - 1, self.size // 2]
            player1_val = 1
            player2_val = 2
            self.board[0, self.size // 2] = (player1_walls, player1_val)
            self.board[self.size - 1, self.size // 2] = (player2_walls, player2_val)

            self.player1 = ([0, self.size // 2], self.board[0, self.size // 2])
            self.player2 = ([self.size - 1, self.size // 2], self.board[self.size - 1, self.size // 2])
        


    # To place a wall use the coordinates of two directly-diagonal board spaces as the first two parameters for the place_wall function. 
    #   These coordinates define the 2x2 grid of cells that the wall will be placed between.
    #   Any two coordinates should work, as long as they are directly diagonal to each other. 
    # The final parameter of the place_wall function is the direction of the wall that will be placed, 0 is for a horizontal wall, 1 is for a vertical wall.

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

    # external game logic should check for valid moves and players before calling this function
    def move_player(self, player_num, direction):
            
            if player_num == 1:
                player = self.player1
            elif player_num == 2:
                player = self.player2
            else:
                raise ValueError("Invalid player number")
            
            player_location = list(player[0])
            
            self.__set_player(player[0], 0)

            if direction == 0: # north
                player_location[0] -= 1               
            elif direction == 1: # east
                player_location[1] += 1     
            elif direction == 2: # south
                player_location[0] += 1  
            elif direction == 3: # west
                player_location[1] -= 1
            else:
                raise ValueError ("Invalid direction")
            
            self.__set_player(player_location, player_num)

            if player_num == 1:
                self.player1 = (player_location, self.board[player_location[0], player_location[1]])
            elif player_num == 2:
                self.player2 = (player_location, self.board[player_location[0], player_location[1]])

    def __set_player(self, location, new_player_num):
        cell_walls = self.board[location[0], location[1]][0]
        self.board[location[0], location[1]] = (cell_walls, new_player_num)

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
    
    def __create_cell(self, r, c, size):
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

    def __str__(self):
        grid_str = ""
        for r in range(self.size):
            row_str = ", ".join(
                f"[{walls.tolist()}, {val}]" for walls, val in self.board[r]
            )
            grid_str += f"{row_str}\n"
        return grid_str
    
    def move_player_jumpaware(self, player_num, target_pos):
        assert isinstance(target_pos, (list, tuple)) and len(target_pos) == 2, f"Invalid target_pos: {target_pos}"

        if player_num == 1:
            old_pos = self.player1[0]
            self.__set_player(old_pos, 0)
            self.__set_player(target_pos, 1)
            self.player1 = (target_pos, self.board[target_pos[0], target_pos[1]])
        elif player_num == 2:
            old_pos = self.player2[0]
            self.__set_player(old_pos, 0)
            self.__set_player(target_pos, 2)
            self.player2 = (target_pos, self.board[target_pos[0], target_pos[1]])
        else:
            raise ValueError("Invalid player number")
        
    def can_move(self, player_num, direction):
        if player_num == 1:
            pos = self.player1[0]
        elif player_num == 2:
            pos = self.player2[0]
        else:
            return False

        r, c = pos
        walls, _ = self.board[r][c]

        # If there's a wall in that direction, can't move
        if walls[direction] == 1:
            return False

        # Determine new position
        move_dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dr, dc = move_dirs[direction]
        new_r, new_c = r + dr, c + dc

        # Check bounds
        if not (0 <= new_r < self.size and 0 <= new_c < self.size):
            return False

        # Check opposite wall in the destination cell
        opposite = (direction + 2) % 4
        neighbor_walls, _ = self.board[new_r][new_c]
        if neighbor_walls[opposite] == 1:
            return False

        return True

### Testing code
#board = BoardState(size=5)

#board.place_wall((0,0), (1,1), 1)

#board.move_player(1, 2)
#board.move_player(2, 1)

#print(board)

#board2 = BoardState(board)
#print(board2)



