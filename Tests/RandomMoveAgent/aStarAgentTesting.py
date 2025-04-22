from boardState import BoardState
from aStarAgent import AStarAgent  # Assuming your class is in astar_agent.py
from astarpathfinding import a_star_path
from astartesting import visualize_path

def run_agent_turn(agent, board_state):
    action, params = agent.choose_action(board_state)
    print(f"\n[AStarAgent] Action chosen by Player {agent.player_num}: {action}, {params}")

    if action == "noop":
        print("Agent chose to do nothing.")
    elif action == "move":
        board_state.move_player(agent.player_num, params["direction"])
    elif action == "move_jumpaware":
        y, x = params["target"]
        board_state.teleport_player(agent.player_num, y, x)
    elif action == "wall":
        c1 = params["corner1"]
        c2 = params["corner2"]
        dir = params["direction"]
        success = board_state.place_wall(c1, c2, dir)
        print(f"Wall placement {'succeeded' if success else 'failed'} at {c1} and {c2}, direction {dir}")

    visualize_path(board_state, a_star_path(board_state, agent.player_num))

def test_astar_agent_behavior():
    print("\n=== A* Agent Test ===")
    board = BoardState(size=5)

    # Move players closer to each other to test interaction
    board.teleport_player(1, 2, 2)
    board.teleport_player(2, 4, 2)

    agent1 = AStarAgent(player_num=1)
    agent2 = AStarAgent(player_num=2)

    print("\nInitial board:")
    visualize_path(board, None)

    # Simulate a few turns
    for turn in range(5):
        print(f"\n--- Turn {turn + 1} ---")
        run_agent_turn(agent1, board)
        run_agent_turn(agent2, board)

if __name__ == "__main__":
    test_astar_agent_behavior()