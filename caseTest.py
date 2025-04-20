from boardState import BoardState
from aStarAgent import AStarAgent

# --------------------------------------------------------------
# This is the implementation for testing the A* agent with 4 test cases mentioned in the test plan documentation
# --------------------------------------------------------------

# Validates if corners are diagonal and within bounds
def is_valid_wall(corner1, corner2, size):
    r1, c1 = corner1
    r2, c2 = corner2
    if not (0 <= r1 < size and 0 <= c1 < size and 0 <= r2 < size and 0 <= c2 < size):
        return False
    return abs(r1 - r2) == 1 and abs(c1 - c2) == 1

# Handles ValueError from bad wall placement
def safe_place_wall(board, corner1, corner2, direction):
    try:
        return board.place_wall(corner1, corner2, direction)
    except ValueError as e:
        print(f"[ERROR] Failed to place wall at {corner1}–{corner2} dir={direction}: {e}")
        return False

# Custom board printer with agent/goal highlight
def print_board(board, agent_pos, goal_pos):
    size = board.size
    for r in range(size):
        row = ""
        for c in range(size):
            if (r, c) == agent_pos:
                row += "A"
            elif (r, c) == goal_pos:
                row += "G"
            elif board.board[r, c].player:
                row += str(board.board[r, c].player)
            else:
                row += "0"
            if c < size - 1:
                wall = board.find_wall(board.board[r, c], board.board[r, c+1], 1)
                row += "\\" if wall.set else "|"
        print(row)
        if r < size - 1:
            row = ""
            for c in range(size):
                wall = board.find_wall(board.board[r, c], board.board[r+1, c], 0)
                row += "\\" if wall.set else "-"
                row += " "
            print(row)

def run_test_case(start_pos, goal_pos, wall_list, case_name):
    print(f"\n=== Running {case_name} ===")
    board = BoardState()

    # Teleport agent and dummy opponent
    board.teleport_player(1, *start_pos)
    board.teleport_player(2, 8, 8)

    # Place walls safely
    for (corner1, corner2, direction) in wall_list:
        if is_valid_wall(corner1, corner2, board.size):
            if not safe_place_wall(board, corner1, corner2, direction):
                print(f"[!] Skipped wall at {corner1}–{corner2}, dir={direction}")
        else:
            print(f"[!] Invalid diagonal: {corner1}–{corner2}")

    # Show board before movement
    print("[Initial Board]")
    print_board(board, start_pos, goal_pos)

    agent = AStarAgent(player_num=1)

    # Loop until agent reaches goal
    steps = 0
    while board.players[0].Y != goal_pos[0] or board.players[0].X != goal_pos[1]:
        action = agent.choose_action(board)
        print(f"[Step {steps}] Action: {action}")

        if action[0] == "move_jumpaware":
            y, x = action[1]["target"]
            board.teleport_player(1, y, x)
            print_board(board, (y, x), goal_pos)
        elif action[0] == "noop":
            print("Agent has no valid move or already at goal.")
            break
        else:
            print(f"Unhandled action: {action}")
            break

        steps += 1
        if steps > 30:
            print("⚠️ Aborting: too many steps (possible loop)")
            break

# --------------------------------------------------------------
# Test Case 1
# Set the board with one wall that blocking the agent’s path, initialize the agent near the goal.
# Test whether the agent can find the shortest path to the goal efficiently
run_test_case(
    start_pos=(1, 4),
    goal_pos=(0, 5),
    wall_list=[
        ((0, 4), (1, 5), 0)
    ],
    case_name="Case 1"
)

# --------------------------------------------------------------
# Test Case 2
# Initialize the agent near the goal while holding multiple walls with no opponent. 
# Test the wall usage efficiency by checking whether the agent can achieve the goal without using any wall .
run_test_case(
    start_pos=(1, 4),
    goal_pos=(0, 5),
    wall_list=[],
    case_name="Case 2"
)

# --------------------------------------------------------------
# Test Case 3
# Set the board with multiple walls that blocking the agent. 
# Test whether the agent can find the shortest path to the goal efficiently.
run_test_case(
    start_pos=(3, 3),
    goal_pos=(0, 3),
    wall_list=[
        ((2, 2), (3, 3), 0),
        ((2, 3), (3, 4), 1),
        ((1, 3), (2, 4), 0),
    ],
    case_name="Case 3"
)

# --------------------------------------------------------------
# Test Case 4
# Set the opponent near its goal. 
# Analyze the agent’s decision-making in wall placemen
run_test_case(
    start_pos=(3, 2),
    goal_pos=(0, 2),
    wall_list=[],
    case_name="Case 4"
)
