import numpy as np
import random
import json
from collections import deque
from boardState import BoardState

# --------------------------------------------------------------
# This is the implementation for a shortest-path moving baseline agent that are used for testing against an AI-driven agent
# The logic for this agent follows the rules of Quoridor
# The agent will spawn on a random square on a random side of the board (0, X), (X, 0), (8, X), (X, 8)
# The goal square for the agent is the corresponding square on the opposite side (e.g if the agent starts at (8, 4), the goal state would be (0, 4))
# Breadth-First Search (BFS) is used for this baseline agent to find the shortest-path 
# --------------------------------------------------------------

class ShortestPathAgent:
    def __init__(self, board: BoardState, player_num: int, start_pos: tuple, goal_pos: tuple):
        self.board = board
        self.player_num = player_num
        self.goal_pos = goal_pos
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Initialize player's position on the board
        self.board.player1 = (list(start_pos), self.board.board[start_pos[0], start_pos[1]])
        self.board.board[start_pos[0], start_pos[1]] = (self.board.board[start_pos[0], start_pos[1]][0], player_num)

    # Using BFS to find the shortest path
    def find_shortest_path(self):
        start = tuple(self.board.player1[0] if self.player_num == 1 else self.board.player2[0])
        visited = set()
        queue = deque([(start, [])])

        while queue:
            position, path = queue.popleft()

            if position == self.goal_pos:
                return path

            if position in visited:
                continue

            visited.add(position)

            possible_moves = self.get_possible_moves(position)
            for new_pos in possible_moves:
                if tuple(new_pos) not in visited:
                    queue.append((tuple(new_pos), path + [new_pos]))

        return []

    # Move along and log the shortest path
    def move_shortest_path(self):
        path = self.find_shortest_path()
        player_pos = list(self.board.player1[0] if self.player_num == 1 else self.board.player2[0])

        movement_log = []

        for step, new_pos in enumerate(path, 1):
            action = (new_pos[0] - player_pos[0], new_pos[1] - player_pos[1])
            direction_idx = self.get_direction_idx(player_pos, new_pos)
            movement_log.append({"current_square": tuple(player_pos), "action": ['N', 'E', 'S', 'W'][direction_idx]})
            self.board.move_player(self.player_num, direction_idx)
            player_pos = new_pos
            print(f"Step {step}: Moved {['N','E','S','W'][direction_idx]} to {player_pos}")

        with open("movement_log.json", "w") as f:
            json.dump(movement_log, f, indent=4)

        if tuple(player_pos) == self.goal_pos:
            print("Reached the goal!")
        else:
            print("Could not find a path to the goal.")

    # Get valid moves including jump over the opponent
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
        if delta in self.directions:
            return self.directions.index(delta)
        else:
            normalized_delta = (np.sign(delta[0]), np.sign(delta[1]))
            return self.directions.index(normalized_delta)

    def valid_move(self, pos):
        return (0 <= pos[0] < self.board.size) and (0 <= pos[1] < self.board.size)


# Randomly select start and goal positions on opposite sides of the board
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


if __name__ == '__main__':
    board_size = 9
    board = BoardState(size=board_size)

    start_pos, goal_position = random_start_and_goal(board_size)
    print(f"Starting position: {start_pos}, Goal position: {goal_position}\n")

    shortest_agent = ShortestPathAgent(board, player_num=1, start_pos=start_pos, goal_pos=goal_position)
    shortest_agent.move_shortest_path()