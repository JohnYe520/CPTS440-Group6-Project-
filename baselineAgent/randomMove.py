import numpy as np
import random
from boardState import BoardState

# This is the implementation for a random moving baseline agent that are used for testing against an AI-driven agent
# The logic for this agent follows the rules of Quoridor
# The agent will spawn on a random square on a random side of the board (0, X), (X, 0), (8, X), (X, 8)
# The goal square for the agent is the corresponding square on the opposite side (e.g if the agent starts at (8, 4), the goal state would be (0, 4))
# Since this is a random moving agent, the maximum steps is set to 50 to avoid potential infinite loop
# However, when testing against the AI agent, the maximum steps should be removed

class RandomMoveAgent:
    def __init__(self, board: BoardState, player_num: int, start_pos: tuple, goal_pos: tuple):
        self.board = board
        self.player_num = player_num
        self.goal_pos = goal_pos
        # Directions represented as (row_change, column_change): North, East, South, West
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        # Initialize player's position on the board
        self.board.player1 = (list(start_pos), self.board.board[start_pos[0], start_pos[1]])
        self.board.board[start_pos[0], start_pos[1]] = (self.board.board[start_pos[0], start_pos[1]][0], player_num)

    def move_randomly(self, max_steps=100):
        steps_taken = 0
        player_pos = list(self.board.player1[0] if self.player_num == 1 else self.board.player2[0])

        # Continue moving randomly until the goal is reached or the step limit is hit
        while steps_taken < max_steps and tuple(player_pos) != self.goal_pos:
            possible_moves = self.get_possible_moves(player_pos)
            if possible_moves:
                new_pos = random.choice(possible_moves)
                direction_idx = self.get_direction_idx(player_pos, new_pos)
                self.board.move_player(self.player_num, direction_idx)
                player_pos = new_pos
                print(f"Step {steps_taken+1}: Moved to {player_pos}")
            else:
                print(f"Step {steps_taken+1}: No valid moves available from {player_pos}")

            steps_taken += 1

        # Report the final status
        if tuple(player_pos) == self.goal_pos:
            print("Reached the goal!")
        else:
            print("Maximum steps reached without reaching goal.")

    def get_possible_moves(self, player_pos):
        possible_moves = []
        for idx, (dr, dc) in enumerate(self.directions):
            new_pos = [player_pos[0] + dr, player_pos[1] + dc]
            if not self.valid_move(new_pos):
                continue

            wall_state, occupant = self.board.board[new_pos[0], new_pos[1]]
            if occupant == 0 and wall_state[(idx + 2) % 4] == 0:
                possible_moves.append(new_pos)
            elif occupant != 0 and wall_state[(idx + 2) % 4] == 0:
                jump_pos = [new_pos[0] + dr, new_pos[1] + dc]
                if self.valid_move(jump_pos):
                    jump_wall_state, jump_occupant = self.board.board[jump_pos[0], jump_pos[1]]
                    if jump_occupant == 0 and wall_state[idx] == 0:
                        possible_moves.append(jump_pos)
                    else:
                        # Lateral moves
                        lateral_dirs = [(dc, dr), (-dc, -dr)]
                        for l_dr, l_dc in lateral_dirs:
                            lateral_pos = [new_pos[0] + l_dr, new_pos[1] + l_dc]
                            if self.valid_move(lateral_pos):
                                lateral_wall_state, lateral_occupant = self.board.board[lateral_pos[0], lateral_pos[1]]
                                if lateral_occupant == 0 and wall_state[(self.get_direction_idx(new_pos, lateral_pos) + 2) % 4] == 0:
                                    possible_moves.append(lateral_pos)
        return possible_moves

    def get_direction_idx(self, old_pos, new_pos):
        delta = (new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])

        # Normalize the delta for jumps or lateral moves
        if delta in self.directions:
            return self.directions.index(delta)
        else:
            # For jumps (two squares away), find intermediate direction
            normalized_delta = (np.sign(delta[0]), np.sign(delta[1]))
            return self.directions.index(normalized_delta)

    # Check if a position is within the boundaries of the board
    def valid_move(self, pos):
        return (0 <= pos[0] < self.board.size) and (0 <= pos[1] < self.board.size)


# Function to randomly select start and goal positions on opposite sides of the board
def random_start_and_goal(size=9):
    side = random.choice(['top', 'bottom', 'left', 'right'])
    pos = random.randint(0, size - 1)

    if side == 'top':
        return (0, pos), (size - 1, pos)
    elif side == 'bottom':
        return (size - 1, pos), (0, pos)
    elif side == 'left':
        return (pos, 0), (pos, size - 1)
    else:  # right
        return (pos, size - 1), (pos, 0)


# Example usage
if __name__ == '__main__':
    board_size = 9
    board = BoardState(size=board_size)

    # Randomly generate start and goal positions
    start_pos, goal_position = random_start_and_goal(board_size)
    print(f"Starting position: {start_pos}, Goal position: {goal_position}\n")

    # Create and run the random-moving agent
    random_agent = RandomMoveAgent(board, player_num=1, start_pos=start_pos, goal_pos=goal_position)
    random_agent.move_randomly(max_steps=50)