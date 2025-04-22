from boardState import BoardState

# advanced logic to represent rules of the game, such as walls blocking movement or jumping over other players
class MoveLogic:
    def __init__(self, *args, size=0):
        self.state = BoardState(args, size)

    def valid_move(self, player_num, direction):
        # if wall is in way or goes off grid, move is not valid
        # check if path is blocked at player location
        if player_num == 1:
            player = self.state.player1[1]
        else:
            player = self.state.player2[1]
        if player[0][direction] == 1:
            return False
        else:
            self.state.move_player(player_num, direction)
        # if direction == 0:
        #     dest = player[0]-1
        # elif direction == 1:
        #     dest = player[1]+1
        # elif direction == 2:
        #     dest = player[0]+1
        # else:
        #     dest = player[1]-1
        # if dest[0] < 0 or dest[0] > self.state.size-1 or dest[1] < 0 or dest[1] > self.state.size-1:
        #     return False
    
    def valid_wall(self, corner1, corner2, direction):
        # if wall already exists, wall is not valid
        dest1 = self.state.board[corner1[0],corner1[1]]
        if direction == 0:
            dest2 = self.state.board[corner1[0],corner2[1]]
            #if corner1[1] > corner2[1]:
              #  dir1 = 
        else:
            dest2 = self.state.board[corner2[0],corner1[1]]
        

