import collections
from astarpathfinding import a_star_path

# --------------------------------------------------------------
# This is the implementation for a baseline BFS agent that is used to test the A* agent.
# --------------------------------------------------------------

class BFSAgent:
    def __init__(self, player_num):
        self.player_num = player_num
        self.opponent_num = 2 if player_num == 1 else 1
        print(f"BFSAgent initialized for Player {self.player_num}")
        
    # Chooses the next action based on the shortest path found by BFS.
    def choose_action(self, board_state):
        # Use the existing a_star_path function which effectively performs BFS
        shortest_path = a_star_path(board_state, self.player_num)

        if not shortest_path:
            y, x = board_state.players[self.player_num - 1].Y, board_state.players[self.player_num - 1].X
            current_space = board_state.board[y][x]
            walls = current_space.get_walls()
            goal_direction = 2 if self.player_num == 1 else 0
            if walls[goal_direction] == 0:
                 # Check if the target space is valid (within bounds)
                 dy, dx = [( -1, 0), (0, 1), (1, 0), (0, -1)][goal_direction]
                 ny, nx = y + dy, x + dx
                 if 0 <= ny < board_state.size and 0 <= nx < board_state.size:
                     # Check if the target space is occupied by the opponent
                     target_space = board_state.board[ny][nx]
                     if target_space.player is None:
                          return ("move_jumpaware", {"target": (ny, nx)})

            # If direct move isn't possible, try any valid move
            for direction, (dy, dx) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                 if walls[direction] == 0:
                     ny, nx = y + dy, x + dx
                     if 0 <= ny < board_state.size and 0 <= nx < board_state.size:
                         target_space = board_state.board[ny][nx]
                         if target_space.player is None:
                            return ("move_jumpaware", {"target": (ny, nx)})

            # If absolutely no move possible
            return ("noop", {})

        if len(shortest_path) < 2:
            # Already at the goal or cannot move
            return ("noop", {})

        # The next position is the second element in the path
        next_pos = shortest_path[1]
        return ("move_jumpaware", {"target": next_pos})

