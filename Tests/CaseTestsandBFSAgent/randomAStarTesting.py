import os
import json
import random
from boardState import BoardState
from aStarAgent import AStarAgent

# Executes a single turn for the given agent and logs moves/walls
def run_agent_turn(agent, board_state, move_log, wall_log):
    action, params = agent.choose_action(board_state)

    if action == "noop":
        return
    elif action == "move":
        board_state.move_player(agent.player_num, params["direction"])
        player = board_state.players[agent.player_num - 1]
        # log position
        move_log.append((player.Y, player.X))
    elif action == "move_jumpaware":
        y, x = params["target"]
        board_state.teleport_player(agent.player_num, y, x)
        move_log.append((y, x))
    elif action == "wall":
        # Log wall history
        wall_log.append((params["corner1"], params["corner2"], params["direction"]))

# Runs multiple self-play games between two AStarAgents and logs results
def test_astar_winrates(num_games=100, board_size=5, turns_per_game=50):
    wins = {1: 0, 2: 0}
    all_game_results = []

    for game_id in range(1, num_games + 1):
        board = BoardState(size=board_size)

        # Random starting positions, avoiding their goal rows
        valid_positions_p1 = [(y, x) for y in range(board_size) for x in range(board_size) if y != board_size - 1]
        valid_positions_p2 = [(y, x) for y in range(board_size) for x in range(board_size) if y != 0]

        start_pos1 = random.choice(valid_positions_p1)
        start_pos2 = random.choice([pos for pos in valid_positions_p2 if pos != start_pos1])

        # Set player positions
        board.teleport_player(1, *start_pos1)
        board.teleport_player(2, *start_pos2)

        # Create agents
        agent1 = AStarAgent(player_num=1)
        agent2 = AStarAgent(player_num=2)

        # Initialize logs for moves and walls
        move_log_1 = [start_pos1]
        move_log_2 = [start_pos2]
        wall_log_1 = []
        wall_log_2 = []

        winner = None
        # Game loop
        for _ in range(turns_per_game):
            run_agent_turn(agent1, board, move_log_1, wall_log_1)
            if board.players[0].Y == board_size - 1:
                wins[1] += 1
                winner = 1
                break

            run_agent_turn(agent2, board, move_log_2, wall_log_2)
            if board.players[1].Y == 0:
                wins[2] += 1
                winner = 2
                break

        all_game_results.append({
            "game_id": game_id,
            "start_positions": {"P1": start_pos1, "P2": start_pos2},
            "move_path": {"P1": move_log_1, "P2": move_log_2},
            "wall_history": {"P1": wall_log_1, "P2": wall_log_2},
            "winner": winner
        })

    # Log the result to a JSON file and store it in the same directory with this file
    output_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "2AStarAgentsTesting.json"
    output_filename = os.path.join(output_dir, file_name)

    print(f"\nAttempting to write results to: {output_filename}")

    try:
        with open(output_filename, 'w') as f:
            json.dump(all_game_results, f, indent=4)
            print(f"\nResults for {len(all_game_results)} games saved to {output_filename}")
    except IOError as e:
        print(f"\nIOError writing results to {output_filename}: {e}")
        print("Please check the path exists and you have write permissions in that directory.")
    except Exception as e:
        print(f"\nAn unexpected error occurred during file writing: {e}")

    # Final winrate printout
    print("\n=== A* Agent Winrate Summary ===")
    print(f"Player 1 Wins: {wins[1]} / {num_games} ({wins[1]/num_games:.2%})")
    print(f"Player 2 Wins: {wins[2]} / {num_games} ({wins[2]/num_games:.2%})")

if __name__ == "__main__":
    test_astar_winrates()
