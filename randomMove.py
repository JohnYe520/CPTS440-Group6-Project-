import numpy as np
import copy
import random
import collections
from boardState import BoardState

# --------------------------------------------------------------
# This is the implementation for a random moving baseline agent that are used for testing against an AI-driven agent
# The logic for this agent follows the rules of Quoridor
# The agent will spawn on a random square on a random side of the board (0, X), (X, 0), (8, X), (X, 8)
# The goal square for the agent is the corresponding square on the opposite side (e.g if the agent starts at (8, 4), the goal state would be (0, 4))
# Since this is a random moving agent, the maximum steps is set to 50 to avoid potential infinite loop
# However, when testing against the AI agent, the maximum steps should be removed
# --------------------------------------------------------------

class RandomMoveAgent:

    def __init__(self, player_num: int):
        self.player_num = player_num
        
        # Directions represented as (row_change, column_change): North, East, South, West
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


    # Move randomly with valid moves 
    def choose_action(self, board_state):
            board_state= BoardState(board_state)
            
            player_pos = []
            player_pos.append(board_state.players[self.player_num - 1].Y)
            player_pos.append(board_state.players[self.player_num - 1].X)
            player_pos = tuple(player_pos)
            #print("player pos: ", player_pos)
            
            possible_moves = self.get_possible_moves(player_pos, board_state)
            #print("possible moves", possible_moves)
            if possible_moves:
                new_pos = random.choice(possible_moves)
                direction_idx = self.get_direction_idx(player_pos, new_pos)
                #board_state.move_player(self.player_num, direction_idx)
                #player_pos = new_pos
                #return ("move_jumpaware", {"target": (ny, nx)})
                
                return ("move_jumpaware", {"target": (new_pos[0], new_pos[1])})
            else:
                #print("no other moves")
                return ("noop", {})


    # Get valid moves including jump over the opponent
    def get_possible_moves(self, player_pos, board_state):
        possible_moves = []
        for idx, (dr, dc) in enumerate(self.directions):

            new_pos = [player_pos[0] + dr, player_pos[1] + dc]
            
            if self.valid_move(new_pos, board_state) == False:
                #print("Invalid  state: ", new_pos)
                continue
            else: 
                #print("Valid state: ", new_pos)
                y, x = board_state.players[self.player_num - 1].Y, board_state.players[self.player_num - 1].X
                current_space = board_state.board[y][x]
                
                #print("Current space: ", current_space)
                wall_state = current_space.get_walls()
                #print ("wall state says walls is:" ,wall_state)
                #print(wall_state)
            
                y_opponent, x_opponent = board_state.players[0].Y, board_state.players[0].X
                #print("opponent :" ,y_opponent, x_opponent)
                opponent_pos = tuple([y_opponent, x_opponent])
                
                #print((idx + 2) % 4)
                #print(wall_state[(idx + 2) % 4])
            
                if wall_state[(idx + 2) % 4] == 0 and opponent_pos != new_pos: # No wall or opponent
                    #print("you are appending ", new_pos, "index = ", idx)
                    possible_moves.append(new_pos)
                
                elif wall_state[(idx + 2) % 4] == 0 and opponent_pos == new_pos: # Jump over the opponent
                    #print("opponent ahead")
                    jump_pos = [new_pos[0] + dr, new_pos[1] + dc]
                    if self.valid_move(jump_pos, board_state):
                        jump_wall_state, jump_occupant = board_state.board[jump_pos[0], jump_pos[1]]
                        if jump_occupant == 0 and wall_state[idx] == 0:
                            possible_moves.append(jump_pos)
                        else: # Sidestep when trying to jump over the wall
                            lateral_dirs = [(dc, dr), (-dc, -dr)]
                            for l_dr, l_dc in lateral_dirs:
                                lateral_pos = [new_pos[0] + l_dr, new_pos[1] + l_dc]
                                if self.valid_move(lateral_pos, board_state):
                                    lateral_wall_state, lateral_occupant = board_state.board[lateral_pos[0], lateral_pos[1]]
                                    if lateral_occupant == 0 and wall_state[(self.get_direction_idx(new_pos, lateral_pos) + 2) % 4] == 0:
                                        possible_moves.append(lateral_pos)
        return possible_moves
            

            
           

    def get_direction_idx(self, old_pos, new_pos):
        delta = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])

        if delta in self.directions:
            return self.directions.index(delta)
        else:
            normalized_delta = (np.sign(delta[0]), np.sign(delta[1]))
            return self.directions.index(normalized_delta)

    def valid_move(self, pos, board_state):
        #print("Checking validity", pos, pos[0], pos[1], board_state.size)
        if (0 <= pos[0] < board_state.size) and (0 <= pos[1] < board_state.size):
            return True
        else:
            return False


# Randomly select start and goal positions on opposite sides of the board
#def random_start_and_goal(size=9):
#    side = random.choice(['top', 'bottom', 'left', 'right'])
#    pos = random.randint(0, size - 1)
#
#    if side == 'top':
#        return (0, pos), (size - 1, pos)
#    elif side == 'bottom':
#        return (size - 1, pos), (0, pos)
#    elif side == 'left':
#        return (pos, 0), (pos, size - 1)
#    else:  # right
#        return (pos, size - 1), (pos, 0)

#if __name__ == '__main__':
#    board_size = 9
#    board = BoardState(size=board_size)
#
#    # Randomly generate start and goal positions
#                    #start_pos, goal_position = random_start_and_goal(board_size)
#                    #print(f"Starting position: {start_pos}, Goal position: {goal_position}\n")

#    #random_agent = RandomMoveAgent(board, player_num=1, start_pos=start_pos, goal_pos=goal_position)
#    random_agent = RandomMoveAgent(board, player_num=1)
#    random_agent.move_randomly(max_steps=50)