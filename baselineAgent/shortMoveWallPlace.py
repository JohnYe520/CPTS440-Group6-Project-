import random
from collections import deque
from boardState import BoardState
from shortMove import ShortestPathAgent

# This is the implementation for a shortest-path moving baseline agent with a basic wall-placement logic that are used for testing against an AI-driven agent
# The logic for this agent follows the rules of Quoridor
# The agent will spawn on a random square on a random side of the board (0, X), (X, 0), (8, X), (X, 8)
# The goal square for the agent is the corresponding square on the opposite side (e.g if the agent starts at (8, 4), the goal state would be (0, 4))
# Breadth-First Search (BFS) is used for this baseline agent to find the shortest-path 

# Wall-placement logic:
#   - calculate the distance between the opponent and its goal
#   - if the distance is less than 5, place a wall in front of the opponent based on the moving direction according to the goal
#   - if the wall-placement is blocked (i.e. wall already exists), the wall should be placed to the left or right or behind the opponent according to its goal.

class WallPlacingAgent:
    def __init__(self, board: BoardState, player_num: int, start_pos: tuple, goal_pos: tuple):
        self.board = board
        self.player_num = player_num
        self.goal_pos = goal_pos
        self.wall_limit = 10
        self.wall_count = 0
        self.wall_log = []  # now stores (turn, top_left, direction)
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.board.player2 = (list(start_pos), self.board.board[start_pos[0], start_pos[1]])
        self.board.board[start_pos[0], start_pos[1]] = (self.board.board[start_pos[0], start_pos[1]][0], player_num)

    def step(self, opponent_agent, current_turn):
        path = opponent_agent.find_shortest_path()
        wall_placed = False

        if len(path) < 5 and self.wall_count < self.wall_limit:
            if path:
                curr = path[0]
                nxt = path[1] if len(path) > 1 else None

                if nxt:
                    dx = nxt[0] - curr[0]
                    dy = nxt[1] - curr[1]

                    if dx != 0:
                        wall_dir = 0
                        top_left = (min(curr[0], nxt[0]), curr[1])
                        wall_placed = self.try_place_wall(top_left, wall_dir, current_turn) or self.try_side_walls(top_left, wall_dir, current_turn)
                    elif dy != 0:
                        wall_dir = 1
                        top_left = (curr[0], min(curr[1], nxt[1]))
                        wall_placed = self.try_place_wall(top_left, wall_dir, current_turn) or self.try_side_walls(top_left, wall_dir, current_turn)

        if not wall_placed:
            self.move_one_step()

    def move_one_step(self):
        path = self.find_shortest_path()
        if path:
            current = self.board.player2[0]
            next_pos = path[0]
            direction = self.get_direction_idx(current, next_pos)
            self.board.move_player(self.player_num, direction)
            print(f"Agent moved to {next_pos}")

    def try_place_wall(self, top_left, direction, turn):
        try:
            self.board.place_wall(top_left, (top_left[0]+1, top_left[1]+1), direction)
            self.wall_count += 1
            self.wall_log.append((turn, top_left, 'H' if direction == 0 else 'V'))
            print(f"Wall placed at {top_left} dir: {'H' if direction == 0 else 'V'} (Turn {turn})")
            return True
        except:
            return False

    def try_side_walls(self, top_left, direction, turn):
        offsets = [(-1, 0), (1, 0)] if direction == 0 else [(0, -1), (0, 1)]
        for dr, dc in offsets:
            shifted = (top_left[0]+dr, top_left[1]+dc)
            if 0 <= shifted[0] < self.board.size-1 and 0 <= shifted[1] < self.board.size-1:
                if self.try_place_wall(shifted, direction, turn):
                    return True
        return False

    def find_shortest_path(self):
        start = tuple(self.board.player2[0])
        visited = set()
        queue = deque([(start, [])])

        while queue:
            pos, path = queue.popleft()
            if pos == self.goal_pos:
                return path
            if pos in visited:
                continue
            visited.add(pos)
            for next_pos in self.get_possible_moves(pos):
                if tuple(next_pos) not in visited:
                    queue.append((tuple(next_pos), path + [next_pos]))
        return []

    def get_possible_moves(self, pos):
        possible = []
        for i, (dr, dc) in enumerate(self.directions):
            nr, nc = pos[0] + dr, pos[1] + dc
            if 0 <= nr < self.board.size and 0 <= nc < self.board.size:
                wall, occ = self.board.board[nr, nc]
                if occ == 0 and wall[(i+2)%4] == 0:
                    possible.append([nr, nc])
        return possible

    def get_direction_idx(self, old, new):
        delta = (new[0] - old[0], new[1] - old[1])
        return self.directions.index(delta)

class ShortestPathStepAgent(ShortestPathAgent):
    def step(self):
        path = self.find_shortest_path()
        if not path:
            return
        current = self.board.player1[0]
        next_pos = path[0]
        direction = self.get_direction_idx(current, next_pos)
        self.board.move_player(self.player_num, direction)
        print(f"Opponent moved to {next_pos}")

def render_board(board):
    for r in range(board.size):
        row = ""
        for c in range(board.size):
            walls, val = board.board[r, c]
            if val == 1:
                row += " 1 "
            elif val == 2:
                row += " 2 "
            elif walls[0] or walls[2]:
                row += " * "
            else:
                row += " . "
        print(row)
    print("\n")

def run_game():
    board = BoardState(size=9)
    p1_start = (0, random.randint(0, 8))
    p1_goal = (8, p1_start[1])
    p2_start = (8, random.randint(0, 8))
    p2_goal = (0, p2_start[1])

    opponent = ShortestPathStepAgent(board, 1, p1_start, p1_goal)
    agent = WallPlacingAgent(board, 2, p2_start, p2_goal)

    print(f"Player 1 starts at {p1_start} -> {p1_goal}")
    print(f"Player 2 starts at {p2_start} -> {p2_goal}")

    for step in range(50):
        print(f"--- Turn {step+1} ---")
        if board.player1[0] == list(p1_goal):
            print("Player 1 reached goal!")
            break
        if board.player2[0] == list(p2_goal):
            print("Player 2 reached goal!")
            break
        opponent.step()
        agent.step(opponent, step+1)
        render_board(board)

if __name__ == '__main__':
    run_game()
